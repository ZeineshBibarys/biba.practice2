import pygame
import random

WIDTH = 400
HEIGHT = 600

def get_image_or_fallback(path, size, color):
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, size)
    except:
        surf = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(surf, color, (0, 0, size[0], size[1]))
        return surf

class Player(pygame.sprite.Sprite):
    def __init__(self, color_name="Blue"):
        super().__init__()
        color_map = {"Blue": (0, 0, 255), "Red": (255, 0, 0), "Green": (0, 255, 0)}
        self.image = get_image_or_fallback('practice 10/resources/player.png', (40, 70), color_map.get(color_name, (0,0,255)))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.speed = 5
        self.shielded = False

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.move_ip(self.speed, 0)
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.shielded:
            pygame.draw.circle(surface, (0, 255, 255), self.rect.center, max(self.rect.width, self.rect.height) // 2 + 5, 3)

class BaseEntity(pygame.sprite.Sprite):
    def __init__(self, size, color, speed, path=''):
        super().__init__()
        self.image = get_image_or_fallback(path, size, color)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.generate_random_pos([])

    def generate_random_pos(self, other_sprites):
        attempts = 0
        while attempts < 50: # Ограничиваем количество попыток, чтобы избежать зависаний
            self.rect.left = random.randint(10, WIDTH - self.rect.width - 10)
            self.rect.bottom = random.randint(-200, -50)
            # Проверяем столкновения, ИГНОРИРУЯ самого себя (s != self)
            if not any(self.rect.colliderect(s.rect.inflate(20, 20)) for s in other_sprites if s != self):
                break
            attempts += 1

    def move(self, other_sprites, speed_multiplier=1.0):
        self.rect.move_ip(0, int(self.speed * speed_multiplier))
        if self.rect.top > HEIGHT:
            self.generate_random_pos(other_sprites)
            return True
        return False

class Enemy(BaseEntity):
    def __init__(self, speed):
        super().__init__((40, 70), (255, 0, 0), speed, 'practice 10/resources/Enemy.png')

class Obstacle(BaseEntity):
    def __init__(self, speed):
        # Represents hazards like oil spills or barriers
        super().__init__((60, 30), (100, 100, 100), speed, '')

class Coin(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 0), (15, 15), 15)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.generate_random_pos([])

    def generate_random_pos(self, other_sprites):
        attempts = 0
        while attempts < 50:
            self.rect.left = random.randint(10, WIDTH - 40)
            self.rect.bottom = random.randint(-500, -50)
            # Проверяем столкновения, ИГНОРИРУЯ самого себя (s != self)
            if not any(self.rect.colliderect(s.rect) for s in other_sprites if s != self):
                break
            attempts += 1

    def move(self, other_sprites, speed_multiplier=1.0):
        self.rect.move_ip(0, int(self.speed * speed_multiplier))
        if self.rect.top > HEIGHT:
            self.generate_random_pos(other_sprites)

    def generate_random_pos(self, other_sprites):
        while True:
            self.rect.left = random.randint(10, WIDTH - 40)
            self.rect.bottom = random.randint(-500, -50)
            if not any(self.rect.colliderect(s.rect) for s in other_sprites):
                break

    def move(self, other_sprites, speed_multiplier=1.0):
        self.rect.move_ip(0, int(self.speed * speed_multiplier))
        if self.rect.top > HEIGHT:
            self.generate_random_pos(other_sprites)

class PowerUp(BaseEntity):
    def __init__(self, speed):
        self.type = random.choice(["nitro", "shield", "repair"])
        colors = {"nitro": (255, 165, 0), "shield": (0, 255, 255), "repair": (0, 255, 0)}
        super().__init__((30, 30), colors[self.type], speed, '')
        
        # Add symbol
        font = pygame.font.SysFont("Verdana", 15, bold=True)
        text = font.render(self.type[0].upper(), True, (0, 0, 0))
        self.image.blit(text, (8, 5))