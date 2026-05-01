import pygame
from persistence import load_settings, save_settings, load_leaderboard
from sprites import WIDTH, HEIGHT

FONT_NAME = "Verdana"

def draw_text(surface, text, size, x, y, color=(255, 255, 255), center=True):
    font = pygame.font.SysFont(FONT_NAME, size, bold=True)
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(rendered, rect)

def draw_button(surface, text, y_pos):
    rect = pygame.Rect(WIDTH//2 - 100, y_pos, 200, 50)
    mouse_pos = pygame.mouse.get_pos()
    color = (100, 100, 100) if rect.collidepoint(mouse_pos) else (50, 50, 50)
    pygame.draw.rect(surface, color, rect, border_radius=10)
    pygame.draw.rect(surface, (255, 255, 255), rect, 2, border_radius=10)
    draw_text(surface, text, 20, WIDTH//2, y_pos + 25)
    return rect

def get_username_screen(screen):
    username = ""
    running = True
    clock = pygame.time.Clock()
    
    while running:
        screen.fill((30, 30, 30))
        draw_text(screen, "Enter Username:", 30, WIDTH//2, HEIGHT//2 - 50)
        draw_text(screen, username + "_", 30, WIDTH//2, HEIGHT//2 + 10, (0, 255, 0))
        draw_text(screen, "Press ENTER to start", 15, WIDTH//2, HEIGHT - 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(username) > 0:
                    return username
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif len(username) < 10 and event.unicode.isprintable():
                    username += event.unicode
                    
        pygame.display.flip()
        clock.tick(30)

def main_menu(screen):
    while True:
        screen.fill((20, 20, 50))
        draw_text(screen, "RACER ADVANCED", 35, WIDTH//2, 100, (255, 215, 0))
        
        btn_play = draw_button(screen, "Play", 200)
        btn_lb = draw_button(screen, "Leaderboard", 270)
        btn_set = draw_button(screen, "Settings", 340)
        btn_quit = draw_button(screen, "Quit", 410)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_play.collidepoint(event.pos): return "play"
                if btn_lb.collidepoint(event.pos): return "leaderboard"
                if btn_set.collidepoint(event.pos): return "settings"
                if btn_quit.collidepoint(event.pos): return "quit"

        pygame.display.flip()

def settings_menu(screen):
    settings = load_settings()
    colors = ["Blue", "Red", "Green"]
    diffs = ["Easy", "Normal", "Hard"]
    
    while True:
        screen.fill((20, 20, 50))
        draw_text(screen, "SETTINGS", 40, WIDTH//2, 80)
        
        btn_snd = draw_button(screen, f"Sound: {'ON' if settings['sound'] else 'OFF'}", 150)
        btn_col = draw_button(screen, f"Car: {settings['car_color']}", 220)
        btn_dif = draw_button(screen, f"Diff: {settings['difficulty']}", 290)
        btn_back = draw_button(screen, "Back", 450)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_snd.collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]
                if btn_col.collidepoint(event.pos):
                    idx = (colors.index(settings["car_color"]) + 1) % len(colors)
                    settings["car_color"] = colors[idx]
                if btn_dif.collidepoint(event.pos):
                    idx = (diffs.index(settings["difficulty"]) + 1) % len(diffs)
                    settings["difficulty"] = diffs[idx]
                if btn_back.collidepoint(event.pos):
                    save_settings(settings)
                    return

        pygame.display.flip()

def leaderboard_menu(screen):
    lb = load_leaderboard()
    while True:
        screen.fill((20, 20, 50))
        draw_text(screen, "TOP 10 SCORES", 35, WIDTH//2, 50, (255, 215, 0))
        
        y = 120
        draw_text(screen, "Rank  Name      Score   Dist", 15, WIDTH//2, 100, (150, 150, 150))
        for i, entry in enumerate(lb):
            text = f"{i+1}. {entry['name'][:8]:<8}  {entry['score']:<6}  {entry['distance']}m"
            draw_text(screen, text, 18, WIDTH//2, y)
            y += 30

        btn_back = draw_button(screen, "Back", HEIGHT - 80)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_back.collidepoint(event.pos): return

        pygame.display.flip()

def game_over_screen(screen, score, dist, coins):
    while True:
        screen.fill((100, 20, 20))
        draw_text(screen, "GAME OVER", 50, WIDTH//2, 100, (255, 0, 0))
        draw_text(screen, f"Final Score: {score}", 25, WIDTH//2, 200)
        draw_text(screen, f"Distance: {dist}m", 25, WIDTH//2, 240)
        draw_text(screen, f"Coins: {coins}", 25, WIDTH//2, 280)

        btn_retry = draw_button(screen, "Retry", 380)
        btn_menu = draw_button(screen, "Main Menu", 450)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_retry.collidepoint(event.pos): return "retry"
                if btn_menu.collidepoint(event.pos): return "menu"

        pygame.display.flip()