import pygame
import random
import sys
from snake_classes import Snake, Food, PowerUp, generate_obstacles, WIDTH, HEIGHT, BLOCK_SIZE
from db import init_db, save_score, get_top_10, get_personal_best
from settings_manager import load_settings, save_settings

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake: Database & Advanced Gameplay")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
UI_FONT = pygame.font.SysFont("Verdana", 20)
TITLE_FONT = pygame.font.SysFont("Verdana", 40, bold=True)

# Initialize DB
init_db()

def draw_text(text, font, color, y, x=WIDTH//2):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x, y))
    screen.blit(surface, rect)

def main_menu():
    username = ""
    active = True
    while active:
        screen.fill(BLACK)
        draw_text("SNAKE ADVANCED", TITLE_FONT, WHITE, 80)
        draw_text("Enter Username:", UI_FONT, WHITE, 160)
        draw_text(username + "_", UI_FONT, (0, 255, 0), 200)
        draw_text("Press ENTER to Play", UI_FONT, GRAY, 260)
        draw_text("1: Leaderboard | 2: Settings | ESC: Quit", UI_FONT, GRAY, 350)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                elif event.key == pygame.K_1:
                    return "leaderboard", username
                elif event.key == pygame.K_2:
                    return "settings", username
                elif event.key == pygame.K_RETURN and len(username) > 0:
                    return "play", username
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif len(username) < 15 and event.unicode.isprintable():
                    username += event.unicode
        pygame.display.flip()
        clock.tick(30)

def settings_screen(settings):
    colors = [(0, 255, 0), (255, 100, 100), (100, 100, 255)] # Green, Red, Blue
    c_idx = colors.index(tuple(settings["snake_color"])) if tuple(settings["snake_color"]) in colors else 0
    
    while True:
        screen.fill(BLACK)
        draw_text("SETTINGS", TITLE_FONT, WHITE, 80)
        draw_text(f"[1] Snake Color: {settings['snake_color']}", UI_FONT, settings["snake_color"], 160)
        draw_text(f"[2] Grid Overlay: {'ON' if settings['grid'] else 'OFF'}", UI_FONT, WHITE, 200)
        draw_text(f"[3] Sound: {'ON' if settings['sound'] else 'OFF'}", UI_FONT, WHITE, 240)
        draw_text("Press BACKSPACE to Save & Return", UI_FONT, GRAY, 350)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    c_idx = (c_idx + 1) % len(colors)
                    settings["snake_color"] = colors[c_idx]
                elif event.key == pygame.K_2:
                    settings["grid"] = not settings["grid"]
                elif event.key == pygame.K_3:
                    settings["sound"] = not settings["sound"]
                elif event.key == pygame.K_BACKSPACE:
                    save_settings(settings)
                    return
        pygame.display.flip()
        clock.tick(30)

def leaderboard_screen():
    scores = get_top_10()
    while True:
        screen.fill(BLACK)
        draw_text("TOP 10", TITLE_FONT, (255, 215, 0), 50)
        
        y = 110
        draw_text("Rank  Name         Score  Lvl", pygame.font.SysFont("Verdana", 15), GRAY, y)
        y += 30
        for i, row in enumerate(scores):
            txt = f"{i+1}. {row[0][:10]:<10}  {row[1]:<5}  {row[2]}"
            draw_text(txt, UI_FONT, WHITE, y)
            y += 25

        draw_text("Press BACKSPACE to Return", UI_FONT, GRAY, HEIGHT - 30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                return
        pygame.display.flip()
        clock.tick(30)

def game_loop(username, settings):
    snake = Snake()
    food = Food()
    powerup = PowerUp()
    
    score = 0
    level = 1
    base_speed = 10
    obstacles = generate_obstacles(level, snake.body)
    food.spawn(snake.body, obstacles)
    
    personal_best = get_personal_best(username)
    foods_eaten = 0
    
    active_powerup = None
    powerup_timer = 0
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: snake.change_direction('UP')
                elif event.key == pygame.K_DOWN: snake.change_direction('DOWN')
                elif event.key == pygame.K_LEFT: snake.change_direction('LEFT')
                elif event.key == pygame.K_RIGHT: snake.change_direction('RIGHT')

        snake.move()

        # Check Food Expiration
        if food.check_expiration():
            food.spawn(snake.body, obstacles)

        # Powerup Spawning Logic
        if not powerup.active and active_powerup is None and random.randint(1, 100) == 1:
            powerup.spawn(snake.body, obstacles, food.position)
        powerup.check_expiration()

        # Handle active powerup expiration
        if active_powerup:
            if pygame.time.get_ticks() - powerup_timer > 5000:
                active_powerup = None # Speed/Slow expires. Shield stays until hit.
                
        # Calculate current speed
        current_speed = base_speed + (level * 2)
        if active_powerup == "speed": current_speed += 5
        elif active_powerup == "slow": current_speed = max(5, current_speed - 5)

        # Food collision
        if snake.body[0] == food.position:
            if food.type == "poison":
                snake.body = snake.body[:-2] # Shorten by 2
                if len(snake.body) <= 1:
                    running = False
            else:
                score += food.weight
                foods_eaten += 1
                if foods_eaten % 4 == 0:
                    level += 1
                    obstacles = generate_obstacles(level, snake.body)
            food.spawn(snake.body, obstacles)
        else:
            snake.body.pop()

        # PowerUp collision
        if powerup.active and snake.body[0] == powerup.position:
            active_powerup = powerup.type
            powerup_timer = pygame.time.get_ticks()
            if active_powerup == "shield": snake.shielded = True
            powerup.active = False

        if len(snake.body) > 0 and snake.check_collision(obstacles):
            running = False

        # Drawing
        screen.fill(BLACK)
        if settings["grid"]:
            for x in range(0, WIDTH, BLOCK_SIZE):
                pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, BLOCK_SIZE):
                pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

        # Draw Obstacles
        for obs in obstacles:
            pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(obs[0], obs[1], BLOCK_SIZE, BLOCK_SIZE))

        # Draw Food & Powerup
        pygame.draw.rect(screen, food.color, pygame.Rect(food.position[0], food.position[1], BLOCK_SIZE, BLOCK_SIZE))
        if powerup.active:
            pygame.draw.rect(screen, powerup.color, pygame.Rect(powerup.position[0], powerup.position[1], BLOCK_SIZE, BLOCK_SIZE))

        # Draw Snake
        for i, pos in enumerate(snake.body):
            color = settings["snake_color"]
            if i == 0 and snake.shielded: color = (0, 0, 255) # Blue head if shielded
            pygame.draw.rect(screen, color, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))

        # UI
        ui_text = UI_FONT.render(f"Score: {score} | Lvl: {level} | PB: {personal_best}", True, WHITE)
        screen.blit(ui_text, (10, 10))
        if active_powerup:
            p_text = UI_FONT.render(f"Buff: {active_powerup.upper()}", True, (0, 255, 255))
            screen.blit(p_text, (WIDTH - 150, 10))

        pygame.display.update()
        clock.tick(current_speed)

    # Game Over
    if score > 0:
        save_score(username, score, level)
    
    while True:
        screen.fill(BLACK)
        draw_text("GAME OVER", TITLE_FONT, (255, 0, 0), 100)
        draw_text(f"Final Score: {score} | Level: {level}", UI_FONT, WHITE, 180)
        draw_text("Press ENTER to Retry | ESC for Menu", UI_FONT, GRAY, 260)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "play"
                if event.key == pygame.K_ESCAPE:
                    return "menu"
        pygame.display.flip()
        clock.tick(30)

def main():
    settings = load_settings()
    action = "menu"
    username = ""

    while True:
        if action == "menu":
            action, username = main_menu()
        elif action == "settings":
            settings_screen(settings)
            action = "menu"
        elif action == "leaderboard":
            leaderboard_screen()
            action = "menu"
        elif action == "play":
            action = game_loop(username, settings)

if __name__ == "__main__":
    main()