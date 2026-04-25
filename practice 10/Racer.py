import pygame
import sys
import time

# Өзіміз жасаған файлдан кластар мен айнымалыларды шақырып алу
from sprites import Player, Enemy, Coin, WIDTH, HEIGHT

# Pygame-ді іске қосу
pygame.init()

# Экран және кадр жиілігі (FPS)
FPS = 60
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer: Екі файлға бөлінген нұсқа")

# Түстер мен Қаріптерді баптау
BLACK = (0, 0, 0)
RED = (255, 0, 0)
font_large = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)

image_game_over = font_large.render("Game Over", True, BLACK)
image_game_over_rect = image_game_over.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Ойын айнымалылары
SCORE = 0
COINS = 0
ENEMY_SPEED = 5

# Суреттер мен дыбыстарды жүктеу
try:
    image_background = pygame.image.load('practice 10/resources/AnimatedStreet.png')
    image_player = pygame.image.load('practice 10/resources/player.png')
    image_enemy = pygame.image.load('practice 10/resources/Enemy.png')
    
    pygame.mixer.music.load('practice 10/resources/background.wav')
    sound_crash = pygame.mixer.Sound('practice 10/resources/crash.wav')
except Exception as e:
    print("Файлдар табылмады! resources папкасын тексеріңіз.", e)
    pygame.quit()
    sys.exit()

# Музыканы шексіз қайталаумен қосу (-1)
pygame.mixer.music.play(-1)

# Спрайттарды (нысандарды) құру
player = Player(image_player)
enemy = Enemy(image_enemy, ENEMY_SPEED)
coin = Coin(ENEMY_SPEED)

# Топтарға бөлу
enemies = pygame.sprite.Group()
enemies.add(enemy)

coins = pygame.sprite.Group()
coins.add(coin)

all_sprites = pygame.sprite.Group()
all_sprites.add(player, enemy, coin)

# Жаулардың жылдамдығын әр 2 секунд сайын арттыру үшін таймер
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 2000)

running = True

# Негізгі ойын циклі
while running:
    # 1. Оқиғаларды өңдеу
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        
        # Жылдамдықты арттыру
        if event.type == INC_SPEED:
            ENEMY_SPEED += 0.5 
            enemy.speed = ENEMY_SPEED
            coin.speed = ENEMY_SPEED

    # 2. Фонды сызу
    screen.blit(image_background, (0, 0))

    # 3. Нысандарды жылжыту және экранға шығару
    for entity in all_sprites:
        # Егер жау болса және ол экраннан сәтті өтсе (ұпай қосылады)
        if isinstance(entity, Enemy):
            if entity.move():
                SCORE += 1
        else:
            entity.move()
            
        screen.blit(entity.image, entity.rect)

    # 4. Ұпайлар мен Тиындар санын көрсету
    score_text = font_small.render(f"Score: {SCORE}", True, BLACK)
    coins_text = font_small.render(f"Coins: {COINS}", True, BLACK)
    screen.blit(score_text, (10, 10))            # Сол жақ бұрыш
    screen.blit(coins_text, (WIDTH - 110, 10))   # Оң жақ бұрыш

    # 5. Соқтығысу: Ойыншы мен Тиын
    if pygame.sprite.spritecollideany(player, coins):
        COINS += 1
        coin.generate_random_pos() # Тиынды жинаған соң қайта жасыру

    # 6. Соқтығысу: Ойыншы мен Жау
    if pygame.sprite.spritecollideany(player, enemies):
        pygame.mixer.music.stop() 
        sound_crash.play()        
        time.sleep(0.5)

        # Ойынның аяқталу экраны
        screen.fill(RED)
        screen.blit(image_game_over, image_game_over_rect)
        pygame.display.update()
        
        time.sleep(2)
        running = False
        pygame.quit()
        sys.exit()

    # Экранды жаңарту
    pygame.display.update()
    clock.tick(FPS)