import random
import pygame

WIDTH = 600
HEIGHT = 400
BLOCK_SIZE = 20

class Snake:
    def __init__(self):
        self.body = [[100, 60], [80, 60], [60, 60]]
        self.direction = 'RIGHT'
        self.shielded = False

    def change_direction(self, new_dir):
        if new_dir == 'UP' and self.direction != 'DOWN': self.direction = 'UP'
        elif new_dir == 'DOWN' and self.direction != 'UP': self.direction = 'DOWN'
        elif new_dir == 'LEFT' and self.direction != 'RIGHT': self.direction = 'LEFT'
        elif new_dir == 'RIGHT' and self.direction != 'LEFT': self.direction = 'RIGHT'

    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == 'UP': head_y -= BLOCK_SIZE
        elif self.direction == 'DOWN': head_y += BLOCK_SIZE
        elif self.direction == 'LEFT': head_x -= BLOCK_SIZE
        elif self.direction == 'RIGHT': head_x += BLOCK_SIZE
        
        self.body.insert(0, [head_x, head_y])

    def check_collision(self, obstacles):
        head = self.body[0]
        collision = False
        is_wall = False
        is_obstacle = False
        obstacle_hit = None
        
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            collision = True
            is_wall = True
        elif head in self.body[1:]:
            collision = True
        else:
            for obs in obstacles:
                if head == obs:
                    collision = True
                    is_obstacle = True
                    obstacle_hit = obs
                    break

        if collision:
            if self.shielded:
                self.shielded = False # Use up the shield
                if is_wall:
                    # Wrap around
                    if head[0] < 0: self.body[0][0] = WIDTH - BLOCK_SIZE
                    elif head[0] >= WIDTH: self.body[0][0] = 0
                    if head[1] < 0: self.body[0][1] = HEIGHT - BLOCK_SIZE
                    elif head[1] >= HEIGHT: self.body[0][1] = 0
                elif is_obstacle:
                    obstacles.remove(obstacle_hit) # Break the block
                return False # Ignore collision this frame
            return True
        return False

class Food:
    def __init__(self):
        self.position = [0, 0]
        self.weight = 1
        self.color = (255, 0, 0)
        self.type = "normal"
        self.spawn_time = 0
        self.duration = 0

    def spawn(self, snake_body, obstacles):
        while True:
            x = random.randrange(0, WIDTH, BLOCK_SIZE)
            y = random.randrange(0, HEIGHT, BLOCK_SIZE)
            if [x, y] not in snake_body and [x, y] not in obstacles:
                self.position = [x, y]
                break
                
        chance = random.randint(1, 100)
        self.spawn_time = pygame.time.get_ticks()
        
        if chance <= 20: # 20% Poison
            self.type = "poison"
            self.weight = 0
            self.color = (139, 0, 0) # Dark Red
            self.duration = 5000
        elif chance <= 40: # 20% Golden
            self.type = "golden"
            self.weight = 3
            self.color = (255, 215, 0)
            self.duration = 4000
        else:
            self.type = "normal"
            self.weight = 1
            self.color = (255, 0, 0)
            self.duration = 0

    def check_expiration(self):
        if self.duration > 0 and pygame.time.get_ticks() - self.spawn_time > self.duration:
            return True
        return False

class PowerUp:
    def __init__(self):
        self.active = False
        self.position = [-100, -100]
        self.type = None
        self.color = (0,0,0)
        self.spawn_time = 0

    def spawn(self, snake_body, obstacles, food_pos):
        if self.active: return
        while True:
            x = random.randrange(0, WIDTH, BLOCK_SIZE)
            y = random.randrange(0, HEIGHT, BLOCK_SIZE)
            if [x, y] not in snake_body and [x, y] not in obstacles and [x, y] != food_pos:
                self.position = [x, y]
                break
        
        self.type = random.choice(["speed", "slow", "shield"])
        colors = {"speed": (0, 255, 255), "slow": (128, 0, 128), "shield": (0, 0, 255)}
        self.color = colors[self.type]
        self.spawn_time = pygame.time.get_ticks()
        self.active = True

    def check_expiration(self):
        if self.active and pygame.time.get_ticks() - self.spawn_time > 8000:
            self.active = False

def generate_obstacles(level, snake_body):
    obstacles = []
    if level < 3: return obstacles
    
    num_blocks = min(5 + (level * 2), 30) # Max 30 blocks
    attempts = 0
    while len(obstacles) < num_blocks and attempts < 100:
        x = random.randrange(0, WIDTH, BLOCK_SIZE)
        y = random.randrange(0, HEIGHT, BLOCK_SIZE)
        
        # Avoid spawning directly near snake head to prevent immediate trap
        head_x, head_y = snake_body[0]
        dist = abs(head_x - x) + abs(head_y - y)
        
        if [x, y] not in snake_body and dist > BLOCK_SIZE * 3:
            obstacles.append([x, y])
        attempts += 1
    return obstacles