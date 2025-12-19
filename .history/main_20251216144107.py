import pygame
from widgets import Button
WIDTH, HEIGHT = 800, 600

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

AI_button = Button(rect=(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50),
                   text="Play vs AI",
                   font=pygame.font.SysFont("Arial", 30),
                   color=(70, 130, 180),
                   hover_color=(100, 149, 237),
                   text_color=(255, 255, 255))


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
        
        pygame.display.flip()
        pygame.display.update()

    pygame.quit()
    
if __name__ == "__main__":
    main()
