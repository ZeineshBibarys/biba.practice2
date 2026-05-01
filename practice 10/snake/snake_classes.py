import random
import pygame

# Экран мен тор (блок) өлшемдері
WIDTH = 600
HEIGHT = 400
BLOCK_SIZE = 20

class Snake:
    def __init__(self):
        # Жыланның бастапқы денесі (3 блоктан тұрады)
        self.body = [[100, 60], [80, 60], [60, 60]]
        self.direction = 'RIGHT'

    def change_direction(self, new_dir):
        # Жылан өзіне қарсы бағытқа бұрыла алмайтынын тексеру
        if new_dir == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        elif new_dir == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        elif new_dir == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        elif new_dir == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'

    def move(self):
        # Бастың қазіргі координатасын алу
        head_x, head_y = self.body[0]

        # Бағытқа байланысты бастың жаңа орнын есептеу
        if self.direction == 'UP':
            head_y -= BLOCK_SIZE
        elif self.direction == 'DOWN':
            head_y += BLOCK_SIZE
        elif self.direction == 'LEFT':
            head_x -= BLOCK_SIZE
        elif self.direction == 'RIGHT':
            head_x += BLOCK_SIZE
        
        # Жаңа басты дененің ең басына қосу (құйрықты алып тастау негізгі циклде шешіледі)
        self.body.insert(0, [head_x, head_y])

    def check_collision(self):
        # Бастың координатасы
        head = self.body[0]
        
        # 1. Қабырғаға (шекараға) соғылуды тексеру
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            return True
            
        # 2. Жыланның өз денесіне соғылуын тексеру
        if head in self.body[1:]:
            return True
            
        return False

class Food:
    def __init__(self):
        self.position = [0, 0]
        self.weight = 1
        self.color = (255, 0, 0) # Қызыл (Қалыпты тамақ)
        self.spawn_time = 0
        self.duration = 0 # 0 = шексіз уақыт

    def spawn(self, snake_body):
        # Тамақтың орнын кездейсоқ таңдау, бірақ ол жыланның денесімен қиылыспауы керек
        while True:
            x = random.randrange(0, WIDTH, BLOCK_SIZE)
            y = random.randrange(0, HEIGHT, BLOCK_SIZE)
            
            # Егер табылған нүкте жыланның үстінде болмаса, оны қабылдаймыз
            if [x, y] not in snake_body:
                self.position = [x, y]
                break
                
        # 30% мүмкіндікпен арнайы (уақытша) тамақ шығару
        chance = random.randint(1, 100)
        if chance <= 30:
            self.weight = 3              # 3 ұпай береді
            self.color = (255, 215, 0)   # Алтын түсті
            self.duration = 4000         # 4 секундтан кейін жоғалады (4000 миллисекунд)
            self.spawn_time = pygame.time.get_ticks()
        else:
            self.weight = 1              # 1 ұпай береді
            self.color = (255, 0, 0)     # Қызыл түсті
            self.duration = 0            # Жоғалмайды

    def check_expiration(self):
        # Егер тамақтың уақыты шектеулі болса, оның мерзімі біткенін тексеру
        if self.duration > 0:
            current_time = pygame.time.get_ticks()
            if current_time - self.spawn_time > self.duration:
                return True
        return False