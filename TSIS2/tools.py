import pygame
from collections import deque

def flood_fill(surface, pos, fill_color):
    """
    Fills a closed region with a target color using Pygame's get_at and set_at.
    Uses BFS to prevent recursion depth errors.
    """
    x, y = pos
    width, height = surface.get_size()
    
    # Ensure starting point is within bounds
    if not (0 <= x < width and 0 <= y < height):
        return

    target_color = surface.get_at((x, y))
    
    # Stop if the region is already the fill color
    if target_color == fill_color:
        return

    queue = deque([(x, y)])
    visited = set([(x, y)])

    while queue:
        cx, cy = queue.popleft()
        
        if 0 <= cx < width and 0 <= cy < height:
            if surface.get_at((cx, cy)) == target_color:
                surface.set_at((cx, cy), fill_color)
                
                # Check neighbors
                for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    nx, ny = cx + dx, cy + dy
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny))

def draw_square(surface, color, start_pos, end_pos, width):
    """Draws a perfect square based on the drag distance."""
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    side = max(abs(dx), abs(dy))
    
    sign_x = 1 if dx >= 0 else -1
    sign_y = 1 if dy >= 0 else -1
    
    rect = pygame.Rect(start_pos[0], start_pos[1], side * sign_x, side * sign_y)
    rect.normalize()
    pygame.draw.rect(surface, color, rect, width)

def draw_right_triangle(surface, color, start_pos, end_pos, width):
    """Draws a right triangle with the right angle at the bottom-left of the drag area."""
    point1 = start_pos
    point2 = (start_pos[0], end_pos[1])
    point3 = end_pos
    pygame.draw.polygon(surface, color, [point1, point2, point3], width)

def draw_equilateral_triangle(surface, color, start_pos, end_pos, width):
    """Draws an equilateral-style triangle."""
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    
    point1 = (start_pos[0] + dx // 2, start_pos[1]) 
    point2 = (start_pos[0], start_pos[1] + dy)      
    point3 = (end_pos[0], start_pos[1] + dy)        
    pygame.draw.polygon(surface, color, [point1, point2, point3], width)

def draw_rhombus(surface, color, start_pos, end_pos, width):
    """Draws a rhombus inside the dragged bounding box."""
    mid_x = (start_pos[0] + end_pos[0]) // 2
    mid_y = (start_pos[1] + end_pos[1]) // 2
    
    point1 = (mid_x, start_pos[1]) 
    point2 = (start_pos[0], mid_y) 
    point3 = (mid_x, end_pos[1])   
    point4 = (end_pos[0], mid_y)   
    
    pygame.draw.polygon(surface, color, [point1, point2, point3, point4], width)