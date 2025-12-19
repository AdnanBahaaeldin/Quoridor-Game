import pygame
from widgets import Button
WIDTH, HEIGHT = 800, 600
button_width = 180
button_height = 50
gap = 20

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quoridor")

def radial_gradient(surface, center, inner_color, outer_color):
    width, height = surface.get_size()
    max_radius = max(width, height)
    for r in range(max_radius, 0, -1):
        ratio = r / max_radius
        color = (
            int(inner_color[0] * ratio + outer_color[0] * (1 - ratio)),
            int(inner_color[1] * ratio + outer_color[1] * (1 - ratio)),
            int(inner_color[2] * ratio + outer_color[2] * (1 - ratio)),
        )
        pygame.draw.circle(surface, color, center, r)
        
logo = pygame.image.load("image.png").convert_alpha()
logo = pygame.transform.smoothscale(logo, (600, 300))
logo_rect = logo.get_rect(midtop=(WIDTH // 2, 20))

buttons_y = logo_rect.bottom + 30
total_width = button_width * 2 + gap
start_x = WIN.get_width() // 2 - total_width // 2
font = pygame.font.SysFont(None, 32)

normal_color = (100, 130, 100)
hover_color = (130, 160, 130)
text_color = (255, 255, 255)

button_play = Button(
    rect=(start_x, buttons_y, button_width, button_height),
    text="New Game",
    font=font,
    color=normal_color,
    hover_color=hover_color,
    text_color=text_color
)

button_quit = Button(
    rect=(start_x + button_width + gap, buttons_y, button_width, button_height),
    text="Continue Playing",
    font=font,
    color=normal_color,
    hover_color=hover_color,
    text_color=text_color
)



def main():
    run = True
    #clock = pygame.time.Clock()

    while run:
        #clock.tick(60)  # 60 FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        WIN.fill((255, 255, 255)) 
        WIN.blit(logo, logo_rect)
        WIN.blit(New_game_button,)
        
        pygame.display.flip()
        pygame.display.update()

    pygame.quit()
    
if __name__ == "__main__":
    main()
