import pygame
from widgets import Button
WIDTH, HEIGHT = 800, 600
button_width = 180
button_height = 50
gap = 20
BOARD_SIZE = 9  
CELL_SIZE = 60  
MARGIN = 50     
BOARD_PIXEL = BOARD_SIZE * CELL_SIZE
WHITE = (245, 245, 220)
BLACK = (0, 0, 0)
WOOD = (180, 140, 100)

pygame.init()
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

normal_color = (120, 92, 58)
hover_color = (172, 142, 104)
text_color = (255, 255, 255)

new_game_button = Button(
    rect=(start_x, buttons_y, button_width, button_height),
    text="New Game",
    font=font,
    color=normal_color,
    hover_color=hover_color,
    text_color=text_color
)

continue_game_button = Button(
    rect=(start_x + button_width + gap, buttons_y, button_width, button_height),
    text="Continue Game",
    font=font,
    color=normal_color,
    hover_color=hover_color,
    text_color=text_color
)

vs_ai_button = Button(
    rect=(start_x, buttons_y, button_width, button_height),
    text="VS AI",
    font=font,
    color=normal_color,
    hover_color=hover_color,
    text_color=text_color
)

vs_human_button = Button(
    rect=(start_x+button_width+gap, buttons_y, button_width, button_height),
    text="VS Human",
    font=font,
    color=normal_color,
    hover_color=hover_color,
    text_color=text_color
)

board_x = (WIN.get_width() - BOARD_PIXEL) // 2
board_y = 100

def main():
    run = True
    state="menu"
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)  # 60 FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if state=="menu":
                if new_game_button.handle_event(event):
                    state="new_game"
                elif continue_game_button.handle_event(event):
                    state="continue_game"
            elif state=="new_game":
                if vs_ai_button.handle_event(event):
                    state="vs_ai"
                if vs_human_button.handle_event(event):
                    state="vs_human"
                
        if state=="menu":
            WIN.fill((255, 255, 255)) 
            WIN.blit(logo, logo_rect)
            new_game_button.draw(WIN)
            continue_game_button.draw(WIN)
            
        elif state=="new_game":
            WIN.fill((255, 255, 255)) 
            WIN.blit(logo, logo_rect)
            vs_ai_button.draw(WIN)
            vs_human_button.draw(WIN)
        
        elif state == "vs_ai":
            WIN.fill((200, 200, 200))
            radial_gradient(WIN, (WIDTH // 2, HEIGHT // 2), (255, 223, 186), (120, 92, 58))
        
        pygame.display.flip()
        pygame.display.update()

    pygame.quit()
    
if __name__ == "__main__":
    main()
