import pygame
from board_game import Board


class Lines(Board):
    def __init__(self, width, height):
        super(Lines, self).__init__(width, height)
        self.set_view(10, 10, 30)
        self.width = width
        self.height = height

    def on_click(self, cell):
        row, col = cell[0], cell[1]
        if self.board[row][col] == 0:
            flag = False
            for r in range(self.height):
                for c in range(self.width):
                    if self.board[r][c] == 1:
                        flag = True
                        if self.has_path(r, c, row, col):
                            self.board[row][col] = -1
                            self.board[r][c] = 0
                            break
            if not flag:
                self.board[row][col] = -1
        elif self.board[row][col] == -1:
            self.board[row][col] = 1
        elif self.board[row][col] == 1:
            self.board[row][col] = -1

    def draw_cell(self, screen, x, y, color=('black', 'red', 'blue')):
        row, col = self.get_cell((x, y))
        pygame.draw.circle(screen, color[self.board[row][col]],
                           (x + self.cell_size // 2, y + self.cell_size // 2), self.cell_size // 2 - 2, 0)

    def voln(self, x, y, cur, n, m, board):
        board[x][y] = cur
        if y + 1 < m:
            if board[x][y + 1] == 0 or (board[x][y + 1] != -1 and board[x][y + 1] > cur):
                self.voln(x, y + 1, cur + 1, n, m, board)
        if x + 1 < n:
            if board[x + 1][y] == 0 or (board[x + 1][y] != -1 and board[x + 1][y] > cur):
                self.voln(x + 1, y, cur + 1, n, m, board)
        if x - 1 >= 0:
            if board[x - 1][y] == 0 or (board[x - 1][y] != -1 and board[x - 1][y] > cur):
                self.voln(x - 1, y, cur + 1, n, m, board)
        if y - 1 >= 0:
            if board[x][y - 1] == 0 or (board[x][y - 1] != -1 and board[x][y - 1] > cur):
                self.voln(x, y - 1, cur + 1, n, m, board)
        return board

    def has_path(self, x1, y1, x2, y2):
        copy_board = []
        for i in range(len(self.board)):
            copy_board.append(self.board[i].copy())
        board = self.voln(x1, y1, 0, self.width, self.height, copy_board)
        if board[x2][y2] > 0:
            return True
        return False


minesweeper = Lines(10, 10)
screen = pygame.display.set_mode((320, 320))
pygame.display.set_caption('Линеечки')
running = True
pygame.font.init()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                minesweeper.get_click(event.pos)
    screen.fill('black')
    minesweeper.render(screen)
    pygame.display.flip()