import pygame

WIDTH, HEIGHT = 800, 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quoridor")



def main():
    run = True
    #clock = pygame.time.Clock()

    while run:
        #clock.tick(60)  # 60 FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        WIN.fill((255, 255, 255))  # Fill the window with white
        pygame.display.update()

    pygame.quit()
    
if __name__ == "__main__":
    main()
