import pygame
import random

# Экран өлшемдері тұрақтылары
WIDTH = 400
HEIGHT = 600

class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.speed = 5

    def move(self):
        # Пернетақта батырмаларын оқу
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
            
        # Ойыншы экран шекарасынан шығып кетпеуін қадағалау
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, speed):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.speed = speed
        self.generate_random_pos()

    def generate_random_pos(self):
        # Жауды жоғарыдан, кездейсоқ X позициясынан шығару
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = 0

    def move(self):
        self.rect.move_ip(0, self.speed)
        # Егер жау экраннан төмен түсіп кетсе
        if self.rect.top > HEIGHT:
            self.generate_random_pos()
            return True # Жаудан сәтті өтті деген белгі (ұпай қосу үшін)
        return False

class Coin(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        # Тиын үшін сары дөңгелек саламыз
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 0), (15, 15), 15)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.generate_random_pos()

    def generate_random_pos(self):
        # Тиынды жоғарыдан, кездейсоқ позициядан шығару
        self.rect.left = random.randint(10, WIDTH - 40)
        self.rect.bottom = random.randint(-100, 0)

    def move(self):
        self.rect.move_ip(0, self.speed)
        # Егер тиын экраннан төмен түсіп кетсе, қайтадан жоғарыдан шығады
        if self.rect.top > HEIGHT:
            self.generate_random_pos()