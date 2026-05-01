import pygame
import sys
import random
from sprites import Player, Enemy, Obstacle, Coin, PowerUp, WIDTH, HEIGHT
from persistence import save_score

def run_game(screen, settings, username):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Verdana", 20)
    
    # Sound setup
    if settings["sound"]:
        try:
            pygame.mixer.music.load('practice 10/resources/background.wav')
            pygame.mixer.music.play(-1)
            crash_sound = pygame.mixer.Sound('practice 10/resources/crash.wav')
        except:
            crash_sound = None
    else:
        pygame.mixer.music.stop()
        crash_sound = None

    # Difficulty Base
    base_speed = {"Easy": 3, "Normal": 5, "Hard": 7}[settings["difficulty"]]
    
    player = Player(settings["car_color"])
    enemies = pygame.sprite.Group(Enemy(base_speed))
    obstacles = pygame.sprite.Group(Obstacle(base_speed))
    coins = pygame.sprite.Group(Coin(base_speed))
    powerups = pygame.sprite.Group()

    all_hazards = pygame.sprite.Group(enemies, obstacles)
    
    score = 0
    coins_collected = 0
    distance = 0.0
    
    active_powerup = None
    powerup_timer = 0
    
    running = True
    speed_multiplier = 1.0

    while running:
        dt = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update difficulty based on distance
        current_speed = base_speed + (distance // 500)
        for e in enemies: e.speed = current_speed
        for o in obstacles: o.speed = current_speed
        
        # Move Player
        player.move()

        # PowerUp Spawning
        if random.randint(1, 600) == 1 and len(powerups) == 0:
            powerups.add(PowerUp(current_speed))

        # Update Powerups
        if active_powerup:
            powerup_timer -= dt
            if powerup_timer <= 0:
                if active_powerup == "nitro":
                    speed_multiplier = 1.0
                active_powerup = None

        # Move Entities
        hazard_list = list(all_hazards)
        for e in enemies:
            if e.move(hazard_list, speed_multiplier): score += 1
        for o in obstacles:
            o.move(hazard_list, speed_multiplier)
        for c in coins:
            c.move(hazard_list, speed_multiplier)
        for p in powerups:
            p.move(hazard_list, speed_multiplier)

        # Distance Calculation
        distance += (current_speed * speed_multiplier) * 0.1

        # Collisions: Coins
        if pygame.sprite.spritecollideany(player, coins):
            coins_collected += 1
            score += 10
            for c in coins: c.generate_random_pos(hazard_list)

        # Collisions: Powerups
        hit_powerup = pygame.sprite.spritecollideany(player, powerups)
        if hit_powerup:
            active_powerup = hit_powerup.type
            if active_powerup == "nitro":
                speed_multiplier = 2.0
                powerup_timer = 4.0
            elif active_powerup == "shield":
                player.shielded = True
                powerup_timer = 10.0 # Time limit or until hit
            elif active_powerup == "repair":
                for h in all_hazards: h.generate_random_pos([])
                score += 50
                active_powerup = None # Instant
            hit_powerup.kill()

        # Collisions: Hazards
        if pygame.sprite.spritecollideany(player, all_hazards):
            if player.shielded:
                player.shielded = False
                active_powerup = None
                for h in all_hazards:
                    if h.rect.colliderect(player.rect):
                        h.generate_random_pos(hazard_list)
            else:
                if crash_sound and settings["sound"]: crash_sound.play()
                pygame.mixer.music.stop()
                running = False

        # Drawing
        screen.fill((50, 50, 50)) # Asphalt fallback color
        
        # Draw road markings
        for y in range(0, HEIGHT, 40):
            pygame.draw.rect(screen, (255, 255, 255), (WIDTH//2 - 5, (y + (distance * 10) % 40), 10, 20))

        for p in powerups: screen.blit(p.image, p.rect)
        for c in coins: screen.blit(c.image, c.rect)
        for o in obstacles: screen.blit(o.image, o.rect)
        for e in enemies: screen.blit(e.image, e.rect)
        player.draw(screen)

        # UI OVERLAY
        total_score = score + (coins_collected * 10) + int(distance)
        texts = [
            f"Score: {total_score}",
            f"Coins: {coins_collected}",
            f"Dist: {int(distance)}m"
        ]
        if active_powerup:
            texts.append(f"[{active_powerup.upper()}] {max(0, int(powerup_timer))}s")

        for i, text in enumerate(texts):
            rendered = font.render(text, True, (255, 255, 255))
            screen.blit(rendered, (10, 10 + i * 25))

        pygame.display.flip()

    # Game Over handling
    save_score(username, total_score, distance)
    return total_score, int(distance), coins_collected