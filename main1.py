import pygame, sys, os


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def draw_text(text, coor, size=25, color='black'):
    font = pygame.font.Font('data/Fixedsys.ttf', size)
    text_coord = coor[0]
    string_rendered = font.render(text, 5, pygame.Color(color))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = text_coord
    intro_rect.x = coor[1]
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)


FPS = 50
pygame.init()
size = WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode(size)
fon_color = pygame.Color('#d5ffd9')
shadow_color = pygame.Color('#a9f0b0')
screen.fill(fon_color)
clock = pygame.time.Clock()
running = True
draw = False
LEVEL = 0  # нужна, чтобы запомнить, какой уровень выбрал пользователь

tile_images = {'grass': load_image('grass.png'), 'tent': load_image('tent.png'),
               'tree': load_image('tree.png'), 'none': load_image('gray.png')}


def terminate():
    pygame.quit()
    sys.exit()


class Button(pygame.sprite.Sprite):
    def __init__(self, group, num, image_name, coor):
        super().__init__(group)
        self.num = num
        self.image = load_image(image_name)
        sizes = self.image.get_size()
        pygame.draw.rect(screen, shadow_color, (coor[0] + 10, coor[1] + 10, sizes[0], sizes[1]), 0)
        self.rect = self.image.get_rect()
        self.rect.x = coor[0]
        self.rect.y = coor[1]

    def update(self, *args):
        global LEVEL
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            if self.num == 0:
                terminate()
            elif self.num == 'menu.png':
                LEVEL = 0
            else:
                LEVEL = self.num


class Cell(pygame.sprite.Sprite):
    def __init__(self, group, image, coor):
        super().__init__(group)
        self.co = coor
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = coor[0] + 2.5
        self.rect.y = coor[1] + 2.5
        # self.counter = 0


class ActiveCell(pygame.sprite.Sprite):
    def __init__(self, group, coor, cell_size):
        super().__init__(group)
        self.co = coor
        self.cell_size = cell_size
        self.counter = 0
        self.sprites = [pygame.transform.scale(tile_images['none'], (self.cell_size - 3, self.cell_size - 3)),
                        pygame.transform.scale(tile_images['grass'], (self.cell_size - 3, self.cell_size - 3)),
                        pygame.transform.scale(tile_images['tent'], (self.cell_size - 10, self.cell_size - 10))]
        self.image = self.sprites[self.counter]
        self.rect = self.image.get_rect()
        self.rect.x = coor[0] + 2.5
        self.rect.y = coor[1] + 2.5

    def update(self, coor):
        # self.image = None
        if coor[0] >= self.co[0] and coor[0] <= self.co[0] + self.cell_size and coor[1] >= self.co[1] and self.co[1] +\
                self.cell_size >= coor[1]:
            if self.counter == 2:
                self.counter = 0
            else:
                self.counter += 1
        self.image = self.sprites[self.counter]


class Board:
    def __init__(self, filename, groups):
        self.groups = groups
        filename = "data/" + filename
        with open(filename, 'r') as mapFile:
            self.board = [line.strip() for line in mapFile]
        self.width = len(self.board[0])
        self.copy = self.board[:]
        if filename == 'data/level1.txt':
            # 5 на 5
            self.levelname = 1
            self.left = 115
            self.top = -25
            self.cell_size = 75
            draw_text('Уровень 1', (10, 450))
        elif filename == 'data/level2.txt':
            # 6 на 6
            self.levelname = 2
            self.left = 125
            self.top = -25
            self.cell_size = 60
            draw_text('Уровень 2', (10, 450))
        elif filename == 'data/level3.txt':
            # 7 на 7
            self.levelname = 3
            self.left = 100
            self.top = -20
            self.cell_size = 60
            draw_text('Уровень 3', (10, 450))

    def render(self):
        for i in range(self.width):
            for j in range(self.width):
                left = self.left + i * self.cell_size
                right = self.top + j * self.cell_size - i * self.cell_size
                if self.board[i][j] == '!' and self.levelname != 3:
                    Cell(self.groups,
                         pygame.transform.scale(tile_images['tree'], (self.cell_size - 3, self.cell_size - 3)),
                         (right + left + 25, left - 25))
                elif self.board[i][j] == '!' and self.levelname == 3:
                    Cell(self.groups,
                         pygame.transform.scale(tile_images['tree'], (self.cell_size - 3, self.cell_size - 3)),
                         (right + left + 20, left - 20))
                else:
                    if self.levelname != 3:
                        ActiveCell(self.groups, (right + left + 25, left - 25), self.cell_size)
                    else:
                        ActiveCell(self.groups, (right + left + 20, left - 20), self.cell_size)
                pygame.draw.rect(screen, pygame.Color('black'), (left, right + left, self.cell_size, self.cell_size), 2)

        for i in range(len(self.board)):
            draw_text(str(self.board[i].count('@')), (-4.9 * self.top + i * self.cell_size, self.left - self.cell_size))
        for j in range(len(self.board)):
            counter = 0
            for i in range(len(self.board)):
                if self.board[i][j] == '@':
                    counter += 1
            draw_text(str(counter), (self.left - self.cell_size, -5 * self.top + j * self.cell_size + 25))

    def get_cell(self, mouse_pos):
        for i in range(self.height):
            for j in range(self.width):
                if i <= (mouse_pos[1] + 30) // 30 <= i + 1 and j <= (mouse_pos[0] + 30) // 30 <= j + 1:
                    return j, i

    def get_click(self, mouse_pos):
        for el in self.groups:
            el.update(mouse_pos)
        self.groups.draw(screen)


def start_screen():
    global LEVEL
    screen.fill(fon_color)
    draw_text('Палатки', (63, 48), 58, 'red')
    draw_text('и', (63, 286), 58)
    draw_text('деревья', (63, 350), 58, '#00ce05')
    draw_text('made by mashaandreeva', (565, 203), 22)
    rules = ['Вам нужно расположить по одной палатке рядом с ', 'каждым деревом. Она должна соприкасаться с ним по ',
             'вертикали или горизонтали. Цифры показывают число ', 'палаток в строке или колонке. Палатки не могут ',
             'соприкасаться даже по диагонали.']
    x = 150
    for el in rules:
        draw_text(el, (x, 20), 23)
        x += 25
    sprites_start_screen = pygame.sprite.Group()
    Button(sprites_start_screen, 'level1.txt', "level1.png", (18, 310))
    Button(sprites_start_screen, 'level2.txt', "level2.png", (217, 310))
    Button(sprites_start_screen, 'level3.txt', "level3.png", (413, 310))
    Button(sprites_start_screen, 0, "quit.png", (160, 520))
    sprites_start_screen.draw(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in sprites_start_screen:
                    button.update(event)
                if LEVEL != 0:
                    return
        pygame.display.flip()
        clock.tick(FPS)


def game():
    global LEVEL, running
    screen.fill(fon_color)
    all_sprites = pygame.sprite.Group()
    cells = pygame.sprite.Group()
    Button(all_sprites, 0, "quit.png", (160, 520))
    Button(all_sprites, 'menu.png', 'menu.png', (8, 8))
    board = Board(LEVEL, cells)
    board.render()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in all_sprites:
                    button.update(event)
                if LEVEL == 0:
                    return
                pos = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0]:
                    board.get_click(pos)
            all_sprites.draw(screen)
            cells.draw(screen)
            pygame.display.flip()


while running:
    start_screen()
    game()
