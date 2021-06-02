import pygame
from .Constant_Vars import RED, WHITE, BLUE, SQUARE_SIZE, ROWS, COLS
from .Checkers_Board import Board
from .Checkers_Piece import Piece
from itertools import product

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
    
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}
        self.boole = True
        self.boole2 = False
        self.color_turn = RED

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            # print ("slected:", row, col, "valid moves:",self.valid_moves)
            if not self.boole:
                # print ("enter")
                valid_moves_list = list(self.valid_moves)
                temp_valid_moves = self.valid_moves
                for x in range(len(valid_moves_list)):
                    # print ("valid moves:", temp_valid_moves)
                    # print ("valid moves list:", valid_moves_list)
                    # print ("current move:", valid_moves_list[x])
                    if temp_valid_moves[valid_moves_list[x]] == []:
                        # print ("enter 2nd")
                        if (x+1) < len(valid_moves_list):
                            continue
                        # print ("changed")
                        self.change_turn()
                        # print ("changed")
                        break
                    else:
                        break
                        
                if not temp_valid_moves: 
                    # print ("changed2")
                    self.change_turn()
                self.boole = True

        
            if self.board.check_king(piece):     
                valid_moves_list = list(self.valid_moves)
                temp_valid_moves = self.valid_moves
                for x in range(len(valid_moves_list)):
                    if temp_valid_moves[valid_moves_list[x]] != []:
                        skipped = self.valid_moves[(valid_moves_list[x])]
                        self.remove = skipped
                        self.boole2 = True
                        break
            print("valid moves:", self.valid_moves)            
            return True
            
        return False

    def _move(self, row, col):
        # print ("row", row)
        # print ("col", col)
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped and not self.boole2:
                self.boole = False
                self.board.remove(skipped)     
            if not skipped and not self.boole2:
                self.change_turn()
                # print ("changed")
            if self.boole2:
                self.board.remove(self.remove)
                self.boole = False
                self.boole2 = False
        else:
            return False
        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED
    
    def check_peice(self):
        for row in range(ROWS):
            for col in range (COLS):
                piece = self.board.get_piece(row, col)
                if piece != 0 and piece.color == self.turn:
                    valid_moves = self.board.get_valid_moves(piece)
                    for move in valid_moves:
                        if valid_moves[move] != []:
                            return True

    
        return False

    def mandatory_eat(self):
        boole = True
        row_list = []
        col_list = []
        # print (self.turn)
        valid_moves = {}
        for row, col in product(range(ROWS), range(COLS)):
            # print (row, col)
            piece = self.board.get_piece(row, col)
            if piece != 0 and piece.color == self.turn:
                valid_moves = self.board.get_valid_moves(piece)
                # print (row,col, "valid moves:", valid_moves)        
                valid_moves_list = list(valid_moves)
                temp_valid_moves = valid_moves

                for x in range(len(valid_moves_list)):
                    if temp_valid_moves[valid_moves_list[x]] != []:
                        # if self.color_turn == RED:
                        #     self.color_turn = WHITE
                        # else:
                        #     self.color_turn = RED
                        boole = False
                        row_list.append(row)
                        col_list.append(col)
                        # return False, row, col

        print (boole,row_list, col_list)
        return boole, row_list, col_list  

    def empty_space(self, row, col):
        piece = self.board.get_piece(row, col)
        if piece == 0:
            return True
        return False
        # valid_moves_list = list(self.valid_moves)
        # for x in range(len(valid_moves_list)):
        #     if self.valid_moves:
        #         if self.valid_moves[valid_moves_list[x]] != []:
        #             for x in range(len(valid_moves_list)):
        #                 print (self.valid_moves[valid_moves_list[x]])
        #                 self.valid_moves[valid_moves_list[x]] = WHITE





