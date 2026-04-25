import pygame
import sys
import math

# Класты шақыру
from paint_classes import Button

pygame.init()

# Экран өлшемдері
WIDTH, HEIGHT = 800, 600
UI_HEIGHT = 60 # Жоғарғы құралдар панелінің биіктігі

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Клоны")

# Түстер тұрақтылары
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Сурет салатын кенепті (canvas) бөлек жасаймыз
# Интерфейспен араласып кетпеуі үшін оның биіктігі UI_HEIGHT-қа қысқа
canvas = pygame.Surface((WIDTH, HEIGHT - UI_HEIGHT))
canvas.fill(WHITE)

font = pygame.font.SysFont("Verdana", 14)

# ---------------------------------------------------------
# Батырмаларды құру
# ---------------------------------------------------------
# Түс таңдау батырмалары
color_buttons = [
    Button(10, 10, 40, 40, RED, RED),
    Button(60, 10, 40, 40, GREEN, GREEN),
    Button(110, 10, 40, 40, BLUE, BLUE),
    Button(160, 10, 40, 40, BLACK, BLACK)
]

# Құрал таңдау батырмалары
tool_buttons = [
    Button(250, 10, 100, 40, WHITE, 'brush', 'Қылқалам'),
    Button(360, 10, 100, 40, WHITE, 'eraser', 'Өшіргіш'),
    Button(470, 10, 100, 40, WHITE, 'rect', 'Төртбұрыш'),
    Button(580, 10, 100, 40, WHITE, 'circle', 'Шеңбер')
]

# Бастапқы күй айнымалылары
current_color = BLACK
current_tool = 'brush'
drawing = False
start_pos = (0, 0)

# ---------------------------------------------------------
# Негізгі цикл
# ---------------------------------------------------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Сол жақ батырмамен шерту
                mouse_pos = event.pos
                
                # Егер тышқан жоғарғы панельде болса (батырмаларды басу)
                if mouse_pos[1] < UI_HEIGHT:
                    for btn in color_buttons:
                        if btn.is_clicked(mouse_pos):
                            current_color = btn.action_value
                            
                    for btn in tool_buttons:
                        if btn.is_clicked(mouse_pos):
                            current_tool = btn.action_value
                
                # Егер тышқан кенептің (ақ қағаздың) үстінде болса
                else:
                    drawing = True
                    # Координатаны кенепке сәйкестендіру (UI биіктігін алып тастаймыз)
                    start_pos = (mouse_pos[0], mouse_pos[1] - UI_HEIGHT)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                drawing = False
                end_pos = (event.pos[0], event.pos[1] - UI_HEIGHT)
                
                # Фигураларды толық салып бітіру (Тышқанды жіберген кезде)
                if current_tool == 'rect':
                    rect_width = end_pos[0] - start_pos[0]
                    rect_height = end_pos[1] - start_pos[1]
                    # Төртбұрыштың координаталарын дұрыстау (теріс мәндер болмауы үшін)
                    r = pygame.Rect(start_pos[0], start_pos[1], rect_width, rect_height)
                    r.normalize()
                    pygame.draw.rect(canvas, current_color, r, 2)
                    
                elif current_tool == 'circle':
                    # Пифагор теоремасы арқылы радиусты есептеу
                    radius = int(math.hypot(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
                    pygame.draw.circle(canvas, current_color, start_pos, radius, 2)

        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                mouse_pos = (event.pos[0], event.pos[1] - UI_HEIGHT)
                
                # Қылқалам мен өшіргіш тышқан қозғалған сайын ізімен сурет салады
                if current_tool == 'brush':
                    pygame.draw.circle(canvas, current_color, mouse_pos, 5)
                elif current_tool == 'eraser':
                    pygame.draw.circle(canvas, WHITE, mouse_pos, 20) # Өшіргіш үлкенірек

    # ---------------------------------------------------------
    # Экранды жаңарту
    # ---------------------------------------------------------
    screen.fill(GRAY) # Панельдің фоны сұр болады
    
    # Кенепті (ақ қағазды) экранның панельден төмен жағына орналастырамыз
    screen.blit(canvas, (0, UI_HEIGHT))

    # Батырмаларды шығару
    for btn in color_buttons:
        btn.draw(screen, font, is_selected=(current_color == btn.action_value))
        
    for btn in tool_buttons:
        btn.draw(screen, font, is_selected=(current_tool == btn.action_value))

    # ---------------------------------------------------------
    # Фигураларды алдын ала көру (Preview) логикасы
    # Бұл қадам фигураны салып жатқанда оның қандай болатынын көру үшін қажет
    # ---------------------------------------------------------
    if drawing and current_tool in ['rect', 'circle']:
        curr_mouse_pos = pygame.mouse.get_pos()
        screen_start_pos = (start_pos[0], start_pos[1] + UI_HEIGHT)
        
        if current_tool == 'rect':
            rect_width = curr_mouse_pos[0] - screen_start_pos[0]
            rect_height = curr_mouse_pos[1] - screen_start_pos[1]
            r = pygame.Rect(screen_start_pos[0], screen_start_pos[1], rect_width, rect_height)
            r.normalize()
            pygame.draw.rect(screen, current_color, r, 2)
            
        elif current_tool == 'circle':
            radius = int(math.hypot(curr_mouse_pos[0] - screen_start_pos[0], curr_mouse_pos[1] - screen_start_pos[1]))
            pygame.draw.circle(screen, current_color, screen_start_pos, radius, 2)

    pygame.display.update()