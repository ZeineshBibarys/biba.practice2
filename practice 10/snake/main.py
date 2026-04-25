import pygame
import sys
import time

# Кластар мен тұрақтыларды шақыру
from snake_classes import Snake, Food, WIDTH, HEIGHT, BLOCK_SIZE

# Pygame-ді іске қосу
pygame.init()

# Экранды баптау
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Жылан ойыны: Деңгейлер мен Жылдамдық")
clock = pygame.time.Clock()

# Түстер
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Қаріптерді (шрифт) баптау
font_ui = pygame.font.SysFont("Verdana", 18)
font_game_over = pygame.font.SysFont("Verdana", 40, bold=True)

# Нысандарды (Объектілерді) құру
snake = Snake()
food = Food()
food.spawn(snake.body) # Алғашқы тамақты шығару

# Ойын айнымалылары
score = 0
level = 1
speed = 10  # Бастапқы жылдамдық
running = True

def show_game_over():
    """Ойын аяқталғанда шығатын экран"""
    screen.fill(BLACK)
    go_text = font_game_over.render("ОЙЫН АЯҚТАЛДЫ", True, RED)
    score_text = font_ui.render(f"Соңғы ұпай: {score} | Жеткен деңгей: {level}", True, WHITE)
    
    screen.blit(go_text, (WIDTH // 2 - go_text.get_width() // 2, HEIGHT // 3))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()

# --- Негізгі ойын циклі ---
while running:
    # 1. Оқиғаларды (басқаруды) өңдеу
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction('UP')
            elif event.key == pygame.K_DOWN:
                snake.change_direction('DOWN')
            elif event.key == pygame.K_LEFT:
                snake.change_direction('LEFT')
            elif event.key == pygame.K_RIGHT:
                snake.change_direction('RIGHT')

    # 2. Жыланды жылжыту
    snake.move()

    # 3. Тамақты жегенін тексеру
    if snake.body[0] == food.position:
        score += 1
        
        # Деңгей көтеру логикасы: Әр 4 тамақ сайын деңгей мен жылдамдық артады
        if score % 4 == 0:
            level += 1
            speed += 2 
            
        food.spawn(snake.body) # Жаңа тамақ шығару
    else:
        # Егер тамақ жемесе, артындағы құйрығын қиып алып тастаймыз (жылан ұзындығы өзгермеуі үшін)
        snake.body.pop()

    # 4. Соқтығысуды (Апатты) тексеру
    if snake.check_collision():
        show_game_over()

    # 5. Экранға сурет салу
    screen.fill(BLACK)
    
    # Жыланды сызу
    for pos in snake.body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
        
    # Тамақты сызу
    pygame.draw.rect(screen, RED, pygame.Rect(food.position[0], food.position[1], BLOCK_SIZE, BLOCK_SIZE))

    # Интерфейс: Ұпай мен Деңгейді экранның сол жақ үстіне шығару
    ui_text = font_ui.render(f"Ұпай: {score} | Деңгей: {level}", True, WHITE)
    screen.blit(ui_text, (10, 10))

    # Экранды жаңарту
    pygame.display.update()
    
    # Кадр жиілігін (Жыланның жылдамдығын) реттеу
    clock.tick(speed)