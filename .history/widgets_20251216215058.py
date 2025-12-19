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

        if self.text and self.font:
            self.text_surf = self.font.render(self.text, True, self.text_color)
            self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        else:
            self.text_surf = None

        if self.image:
            self.image_rect = self.image.get_rect(center=self.rect.center)
       
    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)

        pygame.draw.rect(
            surface,
            self.hover_color if is_hovered else self.color,
            self.rect,
            border_radius=8
        )

        if self.image:
            surface.blit(self.image, self.image_rect)

        if self.text_surf:
            surface.blit(self.text_surf, self.text_rect)

    def handle_event(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

class CircleButton:
    def __init__(self, center, radius, circle_color,hover_color, text="", font=None, text_color=(0,0,0),hover_text_cover=(255,), border_color=None, border_width=0, action=None):
        self.center = center
        self.radius = radius
        self.circle_color = circle_color
        self.hover_color = hover_color
        self.text = text
        self.font = font
        self.text_color = text_color
        self.border_color = border_color
        self.border_width = border_width
        self.action = action  # function to call when clicked

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        # Draw the circle
        pygame.draw.circle(surface, self.hover_color if is_hovered else self.circle_color, self.center, self.radius)
        if self.border_color and self.border_width > 0:
            pygame.draw.circle(surface, self.border_color, self.center, self.radius, self.border_width)
        # Draw the text
        if self.text and self.font:
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=self.center)
            surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        # Check if pos is inside the circle
        x, y = pos
        cx, cy = self.center
        return (x - cx) ** 2 + (y - cy) ** 2 <= self.radius ** 2
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_clicked(event.pos) and self.action:
                self.action()