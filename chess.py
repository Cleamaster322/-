from time import sleep
import os

WHITE = 1
BLACK = 2


def print_board(board):  # Распечатать доску в текстовом виде
    print('     +----+----+----+----+----+----+----+----+')
    for row in range(7, -1, -1):
        print(' ', row + 1, end='  ')
        for col in range(8):
            print('|', board.cell(row, col), end=' ')
        print('|')
        print('     +----+----+----+----+----+----+----+----+')
    print(end='        ')
    for col in range(8):
        print(chr(col + 65), end='    ')
    print()


def correct_coords(row, col):
    return 0 <= row < 8 and 0 <= col < 8


def opponent(color):
    if color == WHITE:
        return BLACK
    else:
        return WHITE


def parse_coords(coords):
    row = int(coords[0][1]) - 1
    col = ord(coords[0][0]) - 65
    row1 = int(coords[1][1]) - 1
    col1 = ord(coords[1][0]) - 65

    return row, col, row1, col1


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = [[None] * 8 for row in range(8)]
        for c in range(8):
            self.field[1][c] = Pawn(WHITE)
            self.field[6][c] = Pawn(BLACK)
            if c == 0 or c == 7:
                self.field[0][c] = Rook(WHITE)
                self.field[7][c] = Rook(BLACK)
            if c == 1 or c == 6:
                self.field[0][c] = Knight(WHITE)
                self.field[7][c] = Knight(BLACK)
            if c == 2 or c == 5:
                self.field[0][c] = Bishop(WHITE)
                self.field[7][c] = Bishop(BLACK)
            if c == 3:
                self.field[0][c] = Queen(WHITE)
                self.field[7][c] = Queen(BLACK)
            if c == 4:
                self.field[0][c] = King(WHITE)
                self.field[7][c] = King(BLACK)

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def get_piece(self, row, col):
        if correct_coords(row, col):
            return self.field[row][col]

    def move_piece(self, row, col, row1, col1):
        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False

        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        else:
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        
        piece_replace = self.get_piece(row1, col1)
        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        if isinstance(piece, Pawn) and (col1 == col + 1 or col1 == col - 1) \
                and (isinstance(self.get_piece(row, col1), Pawn) and self.get_piece(row, col1).passant is True):
            piece_replace = self.get_piece(row, col1)
            self.field[row][col1] = None

        if self.check() is True:
            if isinstance(piece, Pawn) and (col1 == col1 + 1 or col1 == col1 - 1) \
                    and (isinstance(piece_replace, Pawn) and piece_replace.passant is True):
                self.field[row][col1] = piece_replace
            else:
                self.field[row1][col1] = piece_replace
            self.field[row][col] = piece
            if isinstance(piece, Pawn) and piece.passant is True:
                piece.passant = False
            return False
        self.color = opponent(self.color)
        if isinstance(piece, King) or isinstance(piece, Rook):
            piece.moved()
        return True

    def is_under_attack(self, row, col, color):
        for r in range(7, -1, -1):
            for c in range(8):
                piece = self.get_piece(r, c)
                if piece:
                    if piece.get_color() == color and piece.can_attack(self, r, c, row, col):
                        return True

    def promotion(self, row, col, row1, col1, char):
        piece = self.get_piece(row, col)
        if piece.color == WHITE:
            promotion_row = 7
        else:
            promotion_row = 0
        if isinstance(piece, Pawn) and row1 == promotion_row and (piece.can_move(self, row, col, row1, col1)
                                                                  or piece.can_attack(self, row, col, row1, col1)):
            self.field[row][col] = None
            if char == 'R':
                self.field[row1][col1] = Rook(piece.color)
            elif char == 'N':
                self.field[row1][col1] = Knight(piece.color)
            elif char == 'Q':
                self.field[row1][col1] = Queen(piece.color)
            elif char == 'B':
                self.field[row1][col1] = Bishop(piece.color)
            else:
                self.field[row1][col1] = piece
            self.color = opponent(self.color)
            return True

    def check(self):
        for r in range(7, -1, -1):
            for c in range(8):
                piece = self.get_piece(r, c)
                if isinstance(piece, King) and piece.get_color() == self.color:
                    if self.is_under_attack(r, c, opponent(self.color)):
                        return True
                    return False

    def mate(self):
        for r in range(7, -1, -1):
            for c in range(8):
                piece = self.get_piece(r, c)
                if piece and piece.color == self.color:
                    for r1 in range(7, -1, -1):
                        for c1 in range(8):
                            if piece.can_move(self, r, c, r1, c1) or piece.can_attack(self, r, c, r1, c1):
                                piece_replace = self.get_piece(r1, c1)
                                self.field[r][c] = None
                                self.field[r1][c1] = piece
                                if self.check() is False:
                                    self.field[r][c] = piece
                                    self.field[r1][c1] = piece_replace
                                    return False
                                else:
                                    self.field[r][c] = piece
                                    self.field[r1][c1] = piece_replace
        return True

    def clear_passant(self):
        for r in range(7, -1, -1):
            for c in range(8):
                piece = self.get_piece(r, c)
                if isinstance(piece, Pawn) and piece.color == self.color:
                    piece.passant = False

    def castling0(self, rook_col):
        king = self.field[0][4]
        rook = self.field[0][rook_col]
        if isinstance(king, King) and isinstance(rook, Rook) and self.check() is False:
            if king.not_moved is True and rook.not_moved is True:
                if rook_col > 4:
                    step = 1
                else:
                    step = -1
                for c in range(4+step, rook_col, step):
                    if self.get_piece(0, c) is not None:
                        return False
                for c in range(4+step, 4+(step*3), step):
                    if self.is_under_attack(0, c, opponent(king.color)):
                        return False
                self.field[0][4] = None
                self.field[0][rook_col] = None
                if rook_col > 4:
                    self.field[0][6] = king
                    self.field[0][5] = rook
                else:
                    self.field[0][2] = king
                    self.field[0][3] = rook
                rook.moved()
                king.moved()
                return True
        return False

    def castling7(self, rook_col):
        king = self.field[7][4]
        rook = self.field[7][rook_col]
        if isinstance(king, King) and isinstance(rook, Rook) and self.check() is False:
            if king.not_moved is True and rook.not_moved is True:
                if rook_col > 4:
                    step = 1
                else:
                    step = -1
                for c in range(4 + step, rook_col, step):
                    if self.get_piece(7, c) is not None:
                        return False
                for c in range(4 + step, 4 + (step * 3), step):
                    if self.is_under_attack(7, c, opponent(king.color)):
                        return False
                self.field[7][4] = None
                self.field[7][rook_col] = None
                if rook_col > 4:
                    self.field[7][6] = king
                    self.field[7][5] = rook
                else:
                    self.field[7][2] = king
                    self.field[7][3] = rook
                rook.moved()
                king.moved()
                return True
        return False


class Piece:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.not_moved = True

    def char(self):
        return 'R'

    def can_move(self, board, row, col, row1, col1):
        # Невозможно сделать ход в клетку, которая не лежит в том же ряду
        # или столбце клеток.
        if row == row1 and col == col1:
            return False

        if row != row1 and col != col1:
            return False

        step = 1 if (row1 >= row) else -1
        for r in range(row + step, row1 + step, step):
            # Если на пути по горизонтали есть фигура
            piece = board.get_piece(r, col)
            if piece is not None:
                if piece.color == self.color:
                    return False
                elif piece.color == opponent(self.color) and r != row1:
                    return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1 + step, step):
            # Если на пути по вертикали есть фигура
            piece = board.get_piece(row, c)
            if piece is not None:
                if piece.color == self.color:
                    return False
                elif piece.color == opponent(self.color) and c != col1:
                    return False
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

    def moved(self):
        self.not_moved = False


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.passant = False

    def char(self):
        return 'P'

    def can_move(self, board, row, col, row1, col1):
        # Пешка может ходить только по вертикали
        # "взятие на проходе" не реализовано
        # Пешка может сделать из начального положения ход на 2 клетки
        # вперёд, поэтому поместим индекс начального ряда в start_row.
        if self.color == WHITE:
            direction = 1
            start_row = 1
            passant_row = 4
        else:
            direction = -1
            start_row = 6
            passant_row = 5

        # ход на 1 клетку
        if row + direction == row1 and col == col1 and board.field[row1][col1] is None:
            return True

        # ход на 2 клетки из начального положения
        if (row == start_row
                and row + 2 * direction == row1 and col == col1):
            for r in range(row + direction, row1 + direction, direction):
                if board.field[r][col1] is not None:
                    return False
            self.passant = True
            return True

        if row == passant_row and (col1 == col - 1 or col1 == col + 1):
            piece = board.get_piece(row, col1)
            if isinstance(piece, Pawn) and piece.passant is True:
                return True

        return False

    def can_attack(self, board, row, col, row1, col1):
        if self.color == WHITE:
            direction = 1
        else:
            direction = -1
        if row + direction == row1 and abs(col - col1) == 1:
            piece = board.get_piece(row1, col1)
            if piece and piece.color == opponent(self.color):
                return True
        return False


class Knight(Piece):
    def char(self):
        return 'N'

    def can_move(self, board, row, col, row1, col1):
        if row == row1 or col == col1:
            return False
        if abs(row - row1) == 2 and abs(col - col1) == 1:
            piece = board.get_piece(row1, col1)
            if piece is not None:
                if piece.color == self.color:
                    return False

            return True
        if abs(row - row1) == 1 and abs(col - col1) == 2:
            piece = board.get_piece(row1, col1)
            if piece is not None:
                if piece.color == self.color:
                    return False
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Bishop(Piece):
    def char(self):
        return 'B'

    def can_move(self, board, row, col, row1, col1):
        if row == row1 and col == col1:
            return False
        if row + col == row1 + col1 or row - col == row1 - col1:
            r = row
            c = col
            while r != row1 and c != col1:
                if row1 > r and col1 < c:
                    r += 1
                    c -= 1

                elif row1 > r and col1 > c:
                    r += 1
                    c += 1

                elif row1 < r and col1 < c:
                    r -= 1
                    c -= 1

                elif row1 < r and col1 > c:
                    r -= 1
                    c += 1

                piece = board.get_piece(r, c)
                if piece is not None:
                    if piece.color == self.color:
                        return False
                    elif piece.color == opponent(self.color) and (r, c) != (row1, col1):
                        return False
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Queen(Piece):
    def char(self):
        return 'Q'

    def can_move(self, board, row, col, row1, col1):
        if row == row1 and col == col1:
            return False

        if row + col == row1 + col1 or row - col == row1 - col1:
            return Bishop.can_move(self, board, row, col, row1, col1)

        else:
            if row != row1 and col != col1:
                return False

            step = 1 if (row1 >= row) else -1
            for r in range(row + step, row1 + step, step):
                # Если на пути по горизонтали есть фигура
                piece = board.get_piece(r, col)
                if piece is not None:
                    if piece.color == self.color:
                        return False
                    elif piece.color == opponent(self.color) and r != row1:
                        return False

            step = 1 if (col1 >= col) else -1
            for c in range(col + step, col1 + step, step):
                # Если на пути по вертикали есть фигура
                piece = board.get_piece(row, c)
                if piece is not None:
                    if piece.color == self.color:
                        return False
                    elif piece.color == opponent(self.color) and c != col1:
                        return False
            return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.not_moved = True

    def char(self):
        return 'K'

    def can_move(self, board, row, col, row1, col1):
        if row == row1 and col == col1:
            return False

        if abs(row - row1) <= 1 and abs(col - col1) <= 1:
            piece = board.get_piece(row1, col1)
            if piece is not None:
                if piece.color == self.color:
                    return False
            return True
        return False

    def moved(self):
        self.not_moved = False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


def main(stepping):
    # Создаём доску
    board = Board()
    # Цикл ввода команд игроков
    step_c = 0
    len_step = len(stepping)
    while True:
        # Выводим доску
        
        print_board(board)
        if board.check():
            c = ''
            if board.color == WHITE:
                c = 'Белый'
            else:
                c = 'Чёрный'
            print(c + ' король под шахом')
            sleep(2)
            if board.mate():
                print('Мат')

        if board.check() is False:
            if board.mate():
                print('Пат')
        board.clear_passant()

        # # Подсказка по командам
        # print('Команды:')
        # print('    exit                               -- выход')
        # print('    <coord1> <coord2>     -- ход из клетки (coord1) в клетку (coord2)')
        # print('    Короткая рокировка')
        # print('    Длинная рокировка')


        # Выводим чей ход
        if board.current_player_color() == WHITE:
            print('Ход белых: ', end='')
        else:
            print('Ход чёрных: ', end='')
        
        if len_step == step_c:
            command = 'exit'
            for z in range(20):
                print('!')
                sleep(0.2)
            print('Партия окончена')
            return
        else:
            command = stepping[step_c]
        step_c += 1
        if command == 'exit':
            break

        if command == 'shortrock':
            if board.current_player_color() == WHITE:
                if board.castling0(7) is False:
                    print('Рокировка невозможна')
                    continue
            else:
                if board.castling7(7) is False:
                    print('Рокировка невозможна')
                    continue
            board.color = opponent(board.color)
            print()
            continue


        if command == 'longrock':
            if board.current_player_color() == WHITE:
                if board.castling0(0) is False:
                    print('Рокировка невозможна')
                    continue
            else:
                if board.castling7(0) is False:
                    print('Рокировка невозможна')
                    continue
            board.color = opponent(board.color)
            continue

        

        
        command = command.split()
        if len(command) == 3:
            name = command.pop()
            row, col, row1, col1 = parse_coords(command)
            board.promotion(row,col,row1,col1,name)
        else:
            row, col, row1, col1 = parse_coords(command)
        
    
        if board.move_piece(row, col, row1, col1):
            print('Ход успешен')
        else:
            print('Координаты некорректы! Попробуйте другой ход!')
        sleep(1)


f = open('input.txt', 'r')
buf = ''
while True:
    # считываем строку
    line = f.readline()
    # прерываем цикл, если строка пустая
    if not line:
        break
    buf += line
    
li = buf.split('\n')


main(li)

