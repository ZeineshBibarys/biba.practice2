import pygame
import sys
import datetime
import math
from tools import *

# Initialize Pygame
pygame.init()

# Setup Screen and UI dimensions
WIDTH, HEIGHT = 1000, 750
UI_HEIGHT = 100
FPS = 120

# Colors
COLORS = {
    'Black': (0, 0, 0),
    'White': (255, 255, 255),
    'Red': (255, 0, 0),
    'Green': (0, 255, 0),
    'Blue': (0, 0, 255),
    'Yellow': (255, 255, 0),
    'Cyan': (0, 255, 255),
    'Magenta': (255, 0, 255)
}

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSIS 2: Extended Paint Application")
    clock = pygame.time.Clock()
    
    # Fonts
    ui_font = pygame.font.SysFont('Arial', 14, bold=True)
    text_font = pygame.font.SysFont('Arial', 24)

    # Canvas Setup (The drawing layer)
    canvas = pygame.Surface((WIDTH, HEIGHT - UI_HEIGHT))
    canvas.fill(COLORS['White'])

    # Application State
    current_tool = 'pencil'
    current_color = COLORS['Black']
    brush_size = 2
    drawing = False
    start_pos = (0, 0)
    
    # Text Tool State
    text_active = False
    text_input = ""
    text_pos = (0, 0)

    running = True
    while running:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        # Calculate mouse coordinates relative to the canvas
        c_mouse_pos = (mouse_pos[0], mouse_pos[1] - UI_HEIGHT) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # --- KEYBOARD EVENTS ---
            elif event.type == pygame.KEYDOWN:
                # Save Canvas (Ctrl + S)
                if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"canvas_{timestamp}.png"
                    pygame.image.save(canvas, filename)
                    print(f"Canvas saved as {filename}")
                    continue
                
                # Text Tool Handling
                if text_active:
                    if event.key == pygame.K_RETURN:
                        if text_input:
                            t_surf = text_font.render(text_input, True, current_color)
                            canvas.blit(t_surf, text_pos)
                        text_active = False
                        text_input = ""
                    elif event.key == pygame.K_ESCAPE:
                        text_active = False
                        text_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]
                    else:
                        text_input += event.unicode
                    continue

                # Brush Sizes
                if event.key == pygame.K_1: brush_size = 2
                elif event.key == pygame.K_2: brush_size = 5
                elif event.key == pygame.K_3: brush_size = 10

                # Tool Shortcuts
                if event.key == pygame.K_p: current_tool = 'pencil'
                elif event.key == pygame.K_l: current_tool = 'line'
                elif event.key == pygame.K_r: current_tool = 'rect'
                elif event.key == pygame.K_c: current_tool = 'circle'
                elif event.key == pygame.K_s: current_tool = 'square'
                elif event.key == pygame.K_t: current_tool = 'right_tri'
                elif event.key == pygame.K_e: current_tool = 'eq_tri'
                elif event.key == pygame.K_h: current_tool = 'rhombus'
                elif event.key == pygame.K_f: current_tool = 'fill'
                elif event.key == pygame.K_x: current_tool = 'text'
                elif event.key == pygame.K_d: current_tool = 'eraser'

            # --- MOUSE EVENTS ---
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if mouse_pos[1] < UI_HEIGHT:
                        # UI Click: Color Selection
                        x_off = 10
                        for name, color in COLORS.items():
                            if pygame.Rect(x_off, 10, 40, 40).collidepoint(mouse_pos):
                                current_color = color
                            x_off += 50
                    else:
                        # Canvas Click
                        if current_tool == 'fill':
                            # Change cursor to show it's processing (get_at/set_at is slow in Python)
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_WAIT)
                            flood_fill(canvas, c_mouse_pos, current_color)
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        elif current_tool == 'text':
                            text_active = True
                            text_pos = c_mouse_pos
                            text_input = ""
                        else:
                            drawing = True
                            start_pos = c_mouse_pos
                            if current_tool in ['pencil', 'eraser']:
                                color = COLORS['White'] if current_tool == 'eraser' else current_color
                                pygame.draw.circle(canvas, color, start_pos, brush_size // 2)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    drawing = False
                    color = COLORS['White'] if current_tool == 'eraser' else current_color
                    
                    # Finalize Shape on Canvas
                    if current_tool == 'line':
                        pygame.draw.line(canvas, color, start_pos, c_mouse_pos, brush_size)
                    elif current_tool == 'rect':
                        r = pygame.Rect(start_pos[0], start_pos[1], c_mouse_pos[0]-start_pos[0], c_mouse_pos[1]-start_pos[1])
                        r.normalize()
                        pygame.draw.rect(canvas, color, r, brush_size)
                    elif current_tool == 'circle':
                        radius = int(math.hypot(c_mouse_pos[0]-start_pos[0], c_mouse_pos[1]-start_pos[1]))
                        pygame.draw.circle(canvas, color, start_pos, radius, brush_size)
                    elif current_tool == 'square': 
                        draw_square(canvas, color, start_pos, c_mouse_pos, brush_size)
                    elif current_tool == 'right_tri': 
                        draw_right_triangle(canvas, color, start_pos, c_mouse_pos, brush_size)
                    elif current_tool == 'eq_tri': 
                        draw_equilateral_triangle(canvas, color, start_pos, c_mouse_pos, brush_size)
                    elif current_tool == 'rhombus': 
                        draw_rhombus(canvas, color, start_pos, c_mouse_pos, brush_size)

            elif event.type == pygame.MOUSEMOTION:
                if drawing and current_tool in ['pencil', 'eraser']:
                    color = COLORS['White'] if current_tool == 'eraser' else current_color
                    pygame.draw.line(canvas, color, start_pos, c_mouse_pos, brush_size)
                    start_pos = c_mouse_pos # Update start position to form a continuous path

        # --- RENDERING ---
        screen.fill((230, 230, 230)) 
        screen.blit(canvas, (0, UI_HEIGHT)) 

        # Live Preview for Shapes (drawn directly to screen, not canvas)
        if drawing and current_tool not in ['pencil', 'eraser', 'fill', 'text']:
            color = current_color
            screen_start = (start_pos[0], start_pos[1] + UI_HEIGHT)
            
            if current_tool == 'line': 
                pygame.draw.line(screen, color, screen_start, mouse_pos, brush_size)
            elif current_tool == 'rect':
                r = pygame.Rect(screen_start[0], screen_start[1], mouse_pos[0]-screen_start[0], mouse_pos[1]-screen_start[1])
                r.normalize()
                pygame.draw.rect(screen, color, r, brush_size)
            elif current_tool == 'circle':
                radius = int(math.hypot(mouse_pos[0]-screen_start[0], mouse_pos[1]-screen_start[1]))
                pygame.draw.circle(screen, color, screen_start, radius, brush_size)
            elif current_tool == 'square': 
                draw_square(screen, color, screen_start, mouse_pos, brush_size)
            elif current_tool == 'right_tri': 
                draw_right_triangle(screen, color, screen_start, mouse_pos, brush_size)
            elif current_tool == 'eq_tri': 
                draw_equilateral_triangle(screen, color, screen_start, mouse_pos, brush_size)
            elif current_tool == 'rhombus': 
                draw_rhombus(screen, color, screen_start, mouse_pos, brush_size)

        # Live Preview for Text
        if text_active:
            cursor = "|" if pygame.time.get_ticks() % 1000 < 500 else ""
            t_surf = text_font.render(text_input + cursor, True, current_color)
            screen.blit(t_surf, (text_pos[0], text_pos[1] + UI_HEIGHT))

        # --- UI DRAWING ---
        x_off = 10
        for name, color in COLORS.items():
            pygame.draw.rect(screen, color, (x_off, 10, 40, 40))
            if color == current_color: 
                pygame.draw.rect(screen, (100, 100, 100), (x_off, 10, 40, 40), 3) 
            x_off += 50

        # UI Text (Split into lines to prevent overlap)
        text_x = 430
        
        status_txt = ui_font.render(f"TOOL: {current_tool.upper()}   |   SIZE: {brush_size}px", True, (0, 0, 0))
        screen.blit(status_txt, (text_x, 15))
        
        keys_1 = ui_font.render("KEYS: P(Pencil), L(Line), R(Rect), C(Circle), S(Square), T(RTri), E(ETri), H(Rhombus)", True, (80, 80, 80))
        screen.blit(keys_1, (text_x, 40))
        
        keys_2 = ui_font.render("F(Fill), X(Text), D(Eraser)   |   1, 2, 3 (Sizes)   |   Ctrl+S (Save Canvas)", True, (80, 80, 80))
        screen.blit(keys_2, (text_x, 65))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()