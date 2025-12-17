import pygame
from widgets import Button, CircleButton
from board import Board
WIDTH, HEIGHT = 800, 600
button_width = 180
button_height = 50
gap = 20
BOARD_SIZE = 9  
CELL_SIZE = 40  
MARGIN = 50     
BOARD_PIXEL = BOARD_SIZE * CELL_SIZE
WHITE = (245, 245, 220)
BLACK = (0, 0, 0)
WOOD = (180, 140, 100)
normal_color = (120, 92, 58)
hover_color = (172, 142, 104)
text_color = (255, 255, 255)
AI_COLOR = (108, 104, 172)
PLAYER_COLOR = (104, 168, 172)
board = None

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quoridor")
        
logo = pygame.image.load("image.png").convert_alpha()
logo = pygame.transform.smoothscale(logo, (600, 300))
logo_rect = logo.get_rect(midtop=(WIDTH // 2, 20))
undo = pygame.image.load("undo-circular-arrow.png").convert_alpha()
undo = pygame.transform.smoothscale(undo, (20, 20))
redo = pygame.image.load("redo-arrow-symbol.png").convert_alpha()
redo = pygame.transform.smoothscale(redo, (20, 20))

buttons_y = logo_rect.bottom + 30
total_width = button_width * 2 + gap
start_x = WIN.get_width() // 2 - total_width // 2
font = pygame.font.SysFont(None, 32)


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

undo_button = Button(
    rect=(5, 5, 30, 30),  
    image=undo, 
    color=(255, 255, 255),
    hover_color=hover_color)

redo_button = Button(   
    rect=(40, 5, 30, 30),  
    image=redo, 
    color=(255, 255, 255),
    hover_color=hover_color)
     
save_button = Button(   
    rect=(70, 5, 60, 30),  
    text="Save", 
    font=pygame.font.SysFont(None, 24),
    color=(255, 255, 255),
    hover_color=hover_color,
    text_color=(0,0,0))    
               
board_x = (WIN.get_width() - BOARD_PIXEL) // 2
board_y = 100

def draw_pawn(surface, row, col, color):
    center_x = board_x + col * CELL_SIZE + CELL_SIZE // 2
    center_y = board_y + row * CELL_SIZE + CELL_SIZE // 2
    radius = CELL_SIZE // 3
    pygame.draw.circle(surface, color, (center_x, center_y), radius)

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
            elif state=="vs_ai":
                if undo_button.handle_event(event):
                    print("Undo clicked")
                
        if state=="menu":
            WIN.fill((255, 255, 255)) 
            WIN.blit(logo, logo_rect)
            new_game_button.draw(WIN)
            continue_game_button.draw(WIN)
            
        elif state=="new_game":
            board = Board()
            WIN.fill((255, 255, 255)) 
            WIN.blit(logo, logo_rect)
            vs_ai_button.draw(WIN)
            vs_human_button.draw(WIN)
        
        elif state == "vs_ai":
            board
            no_walls_player = 10
            no_walls_ai = 10
            WIN.fill((255, 255, 255))
            #draw navbar
            undo_button.draw(WIN)
            redo_button.draw(WIN)
            save_button.draw(WIN)
            # Draw board background
            pygame.draw.rect(WIN,hover_color, (board_x, board_y, BOARD_PIXEL, BOARD_PIXEL))

            # Draw grid lines
            for i in range(BOARD_SIZE + 1):
                # vertical lines
                start_pos = (board_x + i*CELL_SIZE, board_y)
                end_pos = (board_x + i*CELL_SIZE, board_y + BOARD_PIXEL)
                pygame.draw.line(WIN, WHITE, start_pos, end_pos, 4)

                # horizontal lines
                start_pos = (board_x, board_y + i*CELL_SIZE)
                end_pos = (board_x + BOARD_PIXEL, board_y + i*CELL_SIZE)
                pygame.draw.line(WIN, WHITE, start_pos, end_pos, 4)
            
            draw_pawn(WIN, 8, 4, PLAYER_COLOR)  # Player at (8,4)
            draw_pawn(WIN, 0, 4, AI_COLOR) 
            
            player_circle = CircleButton(
                center=(60, 540),
                radius=50,
                circle_color=(255, 255, 255),
                hover_color=PLAYER_COLOR,
                text="Put a wall",
                font=pygame.font.SysFont(None, 24),
                text_color=PLAYER_COLOR,
                border_color=PLAYER_COLOR,
                border_width=5
            )
            player_circle.draw(WIN)
            ai_circle = CircleButton(
                center=(740, 60),
                radius=50,
                circle_color=(255, 255, 255),
                hover_color=AI_COLOR,
                text="Put a wall",
                font=pygame.font.SysFont(None, 24),
                text_color=AI_COLOR,
                border_color=AI_COLOR,
                border_width=5
            )
            ai_circle.draw(WIN)
        
            for i in range(no_walls_player):
                wall_x = 20
                wall_y = 470 - i * 15
                pygame.draw.rect(WIN, PLAYER_COLOR, (wall_x, wall_y, 80, 4))
            for i in range(no_walls_ai):
                wall_x = 700 
                wall_y = 125 + i * 15
                pygame.draw.rect(WIN, AI_COLOR, (wall_x, wall_y, 80, 4))
    
            turn_font = pygame.font.SysFont(None, 32)
            text_surf = font.render("It's {}'s turn".format(board.get_current_player()), True, PLAYER_COLOR if board.get_current_player() == "Human" else AI_COLOR)
            text_rect = text_surf.get_rect(midtop=(WIDTH // 2, 50))    
            WIN.blit(text_surf, text_rect)  
            print(board.get_current_player(),board.get_current_turn())  
        pygame.display.flip()
        pygame.display.update()

    pygame.quit()
    
if __name__ == "__main__":
    main()
