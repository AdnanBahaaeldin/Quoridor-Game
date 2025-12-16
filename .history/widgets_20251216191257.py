import pygame
class Button:
    def __init__(self, rect, text=None, font=None,image=None, color=(100,130,100), hover_color=(130,160,130), text_color=(255, 255, 255)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.image = image
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color

       
    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color

        pygame.draw.rect(surface, current_color, self.rect, border_radius=8)
        surface.blit(self.text_surf, self.text_rect)

    def handle_event(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )
