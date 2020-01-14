import pygame
from pygame import Surface

# # - трава, @ - палатка, ! - дерево

pygame.init()
size = width, height = 501, 501
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('black'))

fps = 100
clock = pygame.time.Clock()
running = True



class Board:
    # создание поля


    # настройка внешнего вида






    def on_click(self, cell_coords):
        print(cell_coords)
        a = screen.get_at((cell_coords[0] * 30 + 1, cell_coords[1] * 30 + 1))
        if pygame.Color('black') == a:
            pygame.draw.rect(screen, pygame.Color('white'), (cell_coords[0] * 30 + 1, cell_coords[1] * 30 + 1, 28, 28))
        else:
            pygame.draw.rect(screen, pygame.Color('black'), (cell_coords[0] * 30 + 1, cell_coords[1] * 30 + 1, 28, 28))

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell is not None:
            self.on_click(cell)

level =
boar = (len(level[0]), 7)
board = Board(boar[0], boar[1])
board.render()
running = True
