import pygame
from .Constant_Vars import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE
from .Checkers_Piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()
    
    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1 

    def get_piece(self, row, col):
        return self.board[row][col]
    
    def check_king(self, piece):
        if piece.king:
            return True

        return False

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        # self.board[row].append(0)
                        self.board[row].append(Piece(row, col, WHITE))
                        # print (self.board[row])
                    elif row > 4:
                        # self.board[row].append(0)
                        self.board[row].append(Piece(row, col, RED))
                        # print (self.board[row])
                    else:
                        self.board[row].append(0)
                        # print (self.board[row])
                else:
                    self.board[row].append(0)
                    # print (self.board[row])
        
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1
    
    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED
        
        return None 
    
    def get_valid_moves(self, piece):
        moves = {}
        rem = []
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row
        check = False
        ent = False

        a = 0
        b = 0
        c = 0
        d = 0 

        if piece.color == RED and not piece.king:
            delete = []
            move_left = self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left)
            move_right = self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right)
            move_leftdown = self._eat_down_left(row +1, min(row+3, ROWS), 1, piece.color, left)
            move_rightdown = self._eat_down_right(row +1, min(row+3, ROWS), 1, piece.color, right)
            move_left_list = list(move_left)
            move_right_list = list(move_right)
            # print ("move left down", move_leftdown)
            # print ("move right down", move_rightdown)
            move_leftdown_list = list(move_leftdown)
            move_rightdown_list = list(move_rightdown)

            if move_leftdown:
                if move_leftdown[move_leftdown_list[0]] != []:
                    moves.update(move_leftdown)
            
            if move_rightdown:
                if move_rightdown[move_rightdown_list[0]] != []:
                    moves.update(move_rightdown)

            if move_left:
                moves.update(move_left)

            if move_right:
                moves.update(move_right)

            if move_left and move_right:
                if move_left[move_left_list[0]] != [] and move_right[move_right_list[0]] != []:
                    moves.update(move_left)
                    moves.update(move_right)
                if move_left[move_left_list[0]] == [] and move_right[move_right_list[0]] == []:                
                    moves.update(move_left)
                    moves.update(move_right)
                if move_left[move_left_list[0]] != [] and move_right[move_right_list[0]] == []:
                    moves.update(move_left)

                if move_left[move_left_list[0]] == [] and move_right[move_right_list[0]] != []:
                    moves.update(move_right)

            # print (moves)
            if moves:
                for count in moves:
                    # print (moves[count])
                    if moves[count] != []:
                        # print ("enter")
                        ent = True

                for rem in moves:
                    if ent:
                        if moves[rem] == []:
                            # print (moves[rem])
                            delete.append(rem)
                            ent = False
                
                for x in delete:
                    if x in moves:
                        moves.pop(x)
                            


            # print("move_left", move_left)
            # print("move_right", move_right)


        if piece.color == WHITE and not piece.king:
            delete = []
            move_left = self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left)
            move_right = self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right)
            move_left_list = list(move_left)
            move_right_list = list(move_right)
            move_leftdown = self._eat_down_left(row -1, max(row-3, -1), -1, piece.color, left)
            move_rightdown = self._eat_down_right(row -1, max(row-3, -1), -1, piece.color, right)
            move_leftdown_list = list(move_leftdown)
            move_rightdown_list = list(move_rightdown)
            if move_leftdown:
                if move_leftdown[move_leftdown_list[0]] != []:
                    moves.update(move_leftdown)
            
            if move_rightdown:
                if move_rightdown[move_rightdown_list[0]] != []:
                    moves.update(move_rightdown)

            if move_left:
                if move_left[move_left_list[0]] != []:
                    moves.update(move_left)
                if move_left[move_left_list[0]] == []:
                    moves.update(move_left)
            if move_right:
                if move_right[move_right_list[0]] != []:
                    moves.update(move_right)
                if move_right[move_right_list[0]] == []:
                    moves.update(move_right)
            if move_left and move_right:
                if move_left[move_left_list[0]] != [] and move_right[move_right_list[0]] != []:
                    moves.update(move_left)
                    moves.update(move_right)
                if move_left[move_left_list[0]] == [] and move_right[move_right_list[0]] == []:                
                    moves.update(move_left)
                    moves.update(move_right)
                if move_left[move_left_list[0]] != [] and move_right[move_right_list[0]] == []:
                    moves.update(move_left)
                if move_left[move_left_list[0]] == [] and move_right[move_right_list[0]] != []:
                    moves.update(move_right)

            if moves:
                for count in moves:
                    # print (moves[count])
                    if moves[count] != []:
                        # print ("enter")
                        ent = True

                for rem in moves:
                    if ent:
                        if moves[rem] == []:
                            # print (moves[rem])
                            delete.append(rem)
                            ent = False
                
                for x in delete:
                    if x in moves:
                        moves.pop(x)
            # print("move_left", move_left)
            # print("move_right", move_right)
        
        if piece.king:
            
            enter_left = True
            enter_right = True
            enter_leftdown = True
            enter_rightdown = True
            for x in range(ROWS):
                move_left = self._traverse_left(row -1-x, -1, -1, piece.color, left-x)
                move_right = self._traverse_right(row -1-x, -1, -1, piece.color, right+x)
                move_leftdown = self._traverse_left(row + 1 + x, ROWS, 1, piece.color, left-x)
                move_rightdown = self._traverse_right(row + 1 + x, ROWS, 1, piece.color, right+x)
                move_left_list = list(move_left)
                move_right_list = list(move_right)
                move_leftdown_list = list(move_leftdown)
                move_rightdown_list = list(move_rightdown)
                
                if move_left:
                    if move_left[move_left_list[0]] != []:
                        enter_left = False
                        enter_right = False
                        enter_leftdown = False
                        enter_rightdown = False
                        a += 1
                    else:
                        a = 0
                if move_right:
                    if move_right[move_right_list[0]] != []:
                        enter_left = False
                        enter_right = False
                        enter_leftdown = False
                        enter_rightdown = False
                        b += 1
                    else:
                        b = 0

                if move_leftdown:
                    if move_leftdown[move_leftdown_list[0]] != []:
                        enter_left = False
                        enter_right = False
                        enter_leftdown = False
                        enter_rightdown = False
                        c += 1
                    else:
                        c = 0

                if move_rightdown:
                    if move_rightdown[move_rightdown_list[0]] != []:
                        enter_left = False
                        enter_right = False
                        enter_leftdown = False
                        enter_rightdown = False
                        d += 1
                    else:
                        d = 0
                
                if a == 2 or b == 2 or c == 2 or d == 2:
                    enter_left = True
                    enter_right = True
                    enter_leftdown = True
                    enter_rightdown = True
                    break
            
            a, b, c, d = 0, 0, 0, 0
            for x in range(ROWS):
                move_left = self._traverse_left(row -1-x, -1, -1, piece.color, left-x)
                move_right = self._traverse_right(row -1-x, -1, -1, piece.color, right+x)
                move_leftdown = self._traverse_left(row + 1 + x, ROWS, 1, piece.color, left-x)
                move_rightdown = self._traverse_right(row + 1 + x, ROWS, 1, piece.color, right+x)
                move_left_list = list(move_left)
                move_right_list = list(move_right)
                move_leftdown_list = list(move_leftdown)
                move_rightdown_list = list(move_rightdown)

                if move_left:
                    if move_left[move_left_list[0]] != []:
                        enter_left = True

                if move_right:
                    if move_right[move_right_list[0]] != []:
                        enter_right = True
                        
                if move_leftdown:
                    if move_leftdown[move_leftdown_list[0]] != []:
                        enter_leftdown = True

                if move_rightdown:
                    if move_rightdown[move_rightdown_list[0]] != []:
                        enter_rightdown = True

                                 

            delete = []
            boole = True
            if enter_left:
                for x in range(ROWS):
                    move_left = self._traverse_left(row -1-x, -1, -1, piece.color, left-x)
                    move_left_list = list(move_left)
                    print ("move left:", move_left)
                    # print ("row:", x)
                    # print ("move left:",move_left)
                    if not move_left:
                        break
                    if move_left:
                        if move_left[move_left_list[0]] != []:
                            # print ("entered")
                            a += 1
                        else:
                            a = 0

                    if check and a != 2:
                        check = False
                        continue
                            

                    if move_left:
                        if move_left[move_left_list[0]] != [] and a != 2:
                            moves.update(move_left)
                            check = True
                            if not boole:
                                rem.append(move_left_list[0])
                            boole = False

                        if move_left[move_left_list[0]] == [] and a != 2:
                            moves.update(move_left)
                            if boole:
                                rem.append(move_left_list[0])

                    if a == 2:
                        moves.pop(move_left_list[0])
                        move_left.pop(move_left_list[0])
                        boole = True
                        break     
            
                if not boole:                
                    for remove in rem:
                        if remove in moves:
                            moves.pop(remove)

                rem = []        
                boole = True
                check = False

            if enter_right:
                for x in range(ROWS):
                    move_right = self._traverse_right(row -1-x, -1, -1, piece.color, right+x)
                    move_right_list = list(move_right)
                    print("move_right:", move_right)
                    if not move_right:
                        break

                    if move_right:
                        if move_right[move_right_list[0]] != []:
                            b += 1
                        else:
                            b = 0

                    if check and b != 2:
                        check = False
                        continue

                    if move_right:
                        if move_right[move_right_list[0]] != [] and b != 2:
                            moves.update(move_right)
                            check = True
                            if not boole:
                                rem.append(move_right_list[0])
                            boole = False

                        if move_right[move_right_list[0]] == [] and b != 2:
                            moves.update(move_right)
                            if boole:
                                rem.append(move_right_list[0])  

                    if b == 2:
                        moves.pop(move_right_list[0])
                        move_right.pop(move_right_list[0])
                        boole = True
                        break

                if not boole:                
                    for remove in rem:
                        if remove in moves:
                            moves.pop(remove)

                rem = []       
                boole = True
                check = False
            if enter_leftdown:
                for x in range(ROWS):
                    move_leftdown = self._traverse_left(row + 1 + x, ROWS, 1, piece.color, left-x)
                    move_leftdown_list = list(move_leftdown)
                    print ("move leftdown:",move_leftdown)

                    if not move_leftdown:
                        break

                    if move_leftdown:
                        if move_leftdown[move_leftdown_list[0]] != []:
                            # print ("entered")
                            c += 1
                        else:
                            c = 0


                    if check and c != 2:
                        check = False
                        continue

                    if move_leftdown:
                        if move_leftdown[move_leftdown_list[0]] != [] and c != 2:
                            moves.update(move_leftdown)
                            check = True
                            if not boole:
                                rem.append(move_leftdown_list[0])
                            boole = False
                            
                        if move_leftdown[move_leftdown_list[0]] == [] and c != 2:
                            moves.update(move_leftdown)                
                            if boole:
                                rem.append(move_leftdown_list[0])
                    if c == 2:
                        moves.pop(move_leftdown_list[0])
                        move_leftdown.pop(move_leftdown_list[0])
                        boole = True
                        break                                

                if not boole:                
                    for remove in rem:
                        if remove in moves:
                            moves.pop(remove)
                            
                rem = []        
                boole = True
                check = False
            
            if enter_rightdown:
                for x in range(ROWS):
                    move_rightdown = self._traverse_right(row + 1 + x, ROWS, 1, piece.color, right+x)
                    move_rightdown_list = list(move_rightdown)
                    print ("move rightdown:",move_rightdown)
                    
                    if not move_rightdown:
                        break

                    if move_rightdown:
                        if move_rightdown[move_rightdown_list[0]] != []:
                            d += 1
                        else:
                            d = 0

                    if check and d != 2:
                        check = False
                        continue

                    if move_rightdown:
                        if move_rightdown[move_rightdown_list[0]] != [] and d != 2:
                            moves.update(move_rightdown)
                            check = True
                            if not boole:
                                rem.append(move_rightdown_list[0])                        
                            boole = False

                        if move_rightdown[move_rightdown_list[0]] == [] and d != 2:
                            moves.update(move_rightdown)         
                            if boole:
                                rem.append(move_rightdown_list[0])

                    if d == 2:
                        moves.pop(move_rightdown_list[0])
                        move_rightdown.pop(move_rightdown_list[0])
                        boole = True
                        break

                if not boole:                
                    for remove in rem:
                        if remove in moves:
                            moves.pop(remove)
                            
                rem = []        
                boole = True
                check = False

        # print ("moves", moves)
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        # print ("left(before):", left)
        for r in range(start, stop, step):
            # print ("Last(left):",last)
            if left < 0:
                break
        
            current = self.board[r][left]
            # print ("Current(left):", current)
            if current == 0:
                # print ("skipped:",skipped)
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped + skipped
                else:
                    moves[(r, left)] = last
                # print ("Last:",last)

                # if last:
                #     if step == -1:
                #         row = max(r-3, 0)
                #     else:
                #         row = min(r+3, ROWS)
                #     moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                #     moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                    
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
            # print ("left(after):", left)
        
        # print ("Moves(left):", moves)
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        # print ("right(before):", right)
        for r in range(start, stop, step):
            # print ("Last(right):",last)
            if right >= COLS:
                break
            
            current = self.board[r][right]
            # print ("Current(right):", current)
            if current == 0:
                # print ("skipped:",skipped)
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped + skipped
                else:
                    moves[(r, right)] = last
                # print ("Last:",last)
                # if last:
                #     if step == -1:
                #         row = max(r-3, 0)
                #     else:
                #         row = min(r+3, ROWS)
                #     moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                #     moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
            # print ("right(after):", right)
        
        # print ("Moves(right):", moves)
        return moves
    


    def _eat_down_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        # print ("left(before):", left)
        for r in range(start, stop, step):
            # print ("Last(left):",last)
            if left < 0:
                break
            
            current = self.board[r][left]
            # print ("Current(left):", current)
            if current == 0:
                if skipped and not last:
                    break
                else:
                    moves[(r, left)] = last + skipped
                # print ("Last:",last)             
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
            # print ("left(after):", left)
        
        # print ("Moves(left):", moves)
        return moves





    def _eat_down_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        # print ("right(before):", right)
        for r in range(start, stop, step):
            # print ("Last(right):",last)
            if right >= COLS:
                break
            
            current = self.board[r][right]
            # print ("Current(right):", current)
            if current == 0:
                if skipped and not last:
                    break
                else:
                    moves[(r,right)] = last + skipped
                # print ("Last:",last)
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
            # print ("right(after):", right)
        
        # print ("Moves(right):", moves)
        return moves

