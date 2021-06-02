# Assets: https://techwithtim.net/wp-content/uploads/2020/09/assets.zip
import pygame
from checkers.Constant_Vars import WIDTH, HEIGHT, SQUARE_SIZE, RED
from checkers.Game_Rules import Game
# from minimax.algorithm import minimax

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('D  A  M  A (Philippine Checkers) by viv')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.winner() != None:

            if game.winner() == (255, 255, 255):
                print("The game winner is White")
            
            if game.winner() == (255, 0, 0):
                print("The game winner is red") 

            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                boole, row_list, col_list = game.mandatory_eat()
                print("row list:", row_list)
                print("col_list:", col_list)
                if not boole and not game.empty_space(row,col):
                    if row in row_list and col in col_list:
                        game.select(row, col)
                    
                else:
                    game.select(row, col)
                # print (boole, row, col) 
                



        game.update()
    
    pygame.quit()

main()