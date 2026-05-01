import pygame
import sys
from ui import main_menu, settings_menu, leaderboard_menu, get_username_screen, game_over_screen
from racer import run_game
from persistence import load_settings
from sprites import WIDTH, HEIGHT

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Racer Advanced - TSIS 3")

    while True:
        choice = main_menu(screen)
        
        if choice == "quit":
            break
        elif choice == "settings":
            settings_menu(screen)
        elif choice == "leaderboard":
            leaderboard_menu(screen)
        elif choice == "play":
            settings = load_settings()
            username = get_username_screen(screen)
            
            if not username: 
                break

            while True: # Retry loop
                score, dist, coins = run_game(screen, settings, username)
                post_action = game_over_screen(screen, score, dist, coins)
                
                if post_action == "menu":
                    break
                elif post_action == "quit":
                    pygame.quit()
                    sys.exit()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()