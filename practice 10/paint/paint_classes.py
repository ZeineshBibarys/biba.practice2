import pygame

class Button:
    def __init__(self, x, y, width, height, color, action_value, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        # action_value - бұл батырманың қызметі (мысалы: түстің коды немесе 'brush', 'eraser' сияқты мәтін)
        self.action_value = action_value 
        self.text = text

    def draw(self, screen, font, is_selected=False):
        # Батырманың ішін бояу
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Егер бұл батырма таңдалып тұрса, оны қызыл қалың жиекпен ерекшелейміз
        border_color = (255, 0, 0) if is_selected else (0, 0, 0) 
        border_width = 3 if is_selected else 1
        pygame.draw.rect(screen, border_color, self.rect, border_width)
        
        # Батырманың мәтінін ортасына туралап шығару
        if self.text:
            text_surface = font.render(self.text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        # Тышқанның координатасы батырманың үстінде ме, соны тексереді
        return self.rect.collidepoint(mouse_pos)