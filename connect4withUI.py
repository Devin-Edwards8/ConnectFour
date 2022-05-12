import pygame
import numpy as np

pygame.init()

WIDTH, HEIGHT = 700, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ConnectFour")

END_FONT = pygame.font.SysFont("comicsans", 40)
BUTTON_FONT = pygame.font.SysFont("comicsans", 20)

FPS = 60
WHITE = (255, 255, 255)
BLACK =  (0,0,0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0,0,255)
XPOS = [50, 150, 250, 350, 450, 550, 650]
YPOS = [150, 250, 350, 450, 550, 650]

BALL_RADIUS = 40
SPACING = 50
VEL = 4

class Chip:
    def __init__(self, x, y, radius, color, vel, pos):
        self.pos = pos
        self.x = XPOS[pos]
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = vel

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def place(self, y):
        self.y = y

    def update_position(self, right):
        if right and self.pos != 6:
            self.pos += 1
        elif not right and self.pos != 0:
            self.pos -= 1
        self.x = XPOS[self.pos]

def draw_board(win):
    pygame.draw.rect(win, BLUE, (0, SPACING * 2, WIDTH, HEIGHT - (BALL_RADIUS * 2)))

    for i in range(1, 15, 2):
        for j in range(3, 15, 2):
            pygame.draw.circle(win, BLACK, (((SPACING) * i), (SPACING) * j), BALL_RADIUS)

def draw(win, chips):
    win.fill(BLACK)

    draw_board(win)

    for chip in chips:
        chip.draw(win)

    pygame.display.update()

def draw_win_screen(win, player):
    win.fill(BLACK)

    end_text = END_FONT.render("Player " + str(player) +  " Wins!", 1, WHITE)
    win.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, 30, 120, 40))

    play_button_text = BUTTON_FONT.render("Press 1 for a rematch!", 1, WHITE)
    win.blit(play_button_text, (WIDTH // 2 - play_button_text.get_width() // 2, HEIGHT // 2, 120, 40))

    pygame.display.update()

def handle_winner(player):
    endscreen = True
    while(endscreen): 
        draw_win_screen(WIN, player)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            key = pygame.key.get_pressed()
            if key[pygame.K_1]:
                endscreen = False
    return True

def create_board():
    board = np.zeros((6,7))
    return board

def column_full(selection, board):
    return board[0][selection] != 0

def place_chip(selection, board, player, chip):
    for x in range(5,-1,-1):
        if board[x][selection] == 0:
            chip.place(YPOS[x])
            board[x][selection] = player
            break

def check_status(board, p):
    for i in range(7):
        for j in range(5,2,-1):
            if board[j][i] == p and board[j-1][i] == p and board[j-2][i] == p and board[j-3][i] == p:
                return True

    for j in range(5,-1,-1):
        for i in range(4):
            if board[j][i] == p and board[j][i+1] == p and board[j][i+2] == p and board[j][i+3] == p:
                return True

    for i in range(4):
        for j in range(5,2,-1):
            if board[j][i] == p and board[j-1][i+1] == p and board[j-2][i+2] == p and board[j-3][i+3] == p:
                return True

    for i in range(6, 2, -1):
        for j in range(5,2,-1):
            if board[j][i] == p and board[j-1][i-1] == p and board[j-2][i-2] == p and board[j-3][i-3] == p:
                return True

def main():
    run = True
    clock = pygame.time.Clock()
    turn = 0
    board = create_board()
    chips = []
    chips.append(Chip(WIDTH//2, SPACING, BALL_RADIUS, RED, VEL, 3))

    while run:
        clock.tick(FPS)
        draw(WIN, chips)
        key = pygame.key.get_pressed()

        if turn % 2 == 0:
            player = 1
        else:
            player = 2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if key[pygame.K_LEFT]:
                chips[turn].update_position(False)
            if key[pygame.K_RIGHT]:
                chips[turn].update_position(True)
            if key[pygame.K_RETURN]:
                if not column_full(chips[turn].pos, board):
                    place_chip(chips[turn].pos, board, player, chips[turn])
                    winner = check_status(board, player)
                    turn += 1
                    if winner:
                        chips.clear()
                        board = np.zeros((6,7))
                        turn = 0
                        again = handle_winner(player)
                        if again:
                            chips.append(Chip(WIDTH//2, SPACING, BALL_RADIUS, RED, VEL, 3))
                            continue
                        else: 
                            run = False
                            break
                    if (turn % 2) == 0:
                        chips.append(Chip(WIDTH//2, SPACING, BALL_RADIUS, RED, VEL, 3))
                    else:
                        chips.append(Chip(WIDTH//2, SPACING, BALL_RADIUS, YELLOW, VEL, 3))


if __name__ == "__main__":
    main()
