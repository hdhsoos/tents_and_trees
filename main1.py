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
screen.fill(pygame.Color('#d5ffd9'))
# очень красивый светло-зелёный (бледно-салатовый) цвет :)
clock = pygame.time.Clock()
running = True
draw = False
LEVEL = 0  # нужна, чтобы запомнить, какой уровень выбрал пользователь

tile_images = {'grass': load_image('grass.png'), 'tent': load_image('tent.png'), 'tree': load_image('tree.png'),
               'none': load_image('gray.png')}


def terminate():
    pygame.quit()
    sys.exit()


class Button(pygame.sprite.Sprite):
    def __init__(self, group, num, image_name, coor):
        super().__init__(group)
        self.num = num
        self.image = load_image(image_name)
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


class Board:
    def __init__(self, filename):
        filename = "data/" + filename
        with open(filename, 'r') as mapFile:
            self.board = [line.strip() for line in mapFile]
        self.width = len(self.board[0])
        if filename == 'data/level1.txt':
            # 5 на 5
            self.left = 115
            self.top = -25
            self.cell_size = 75
            draw_text('Уровень 1', (10, 450))
        elif filename == 'data/level2.txt':
            # 6 на 6
            self.left = 125
            self.top = -25
            self.cell_size = 60
            draw_text('Уровень 2', (10, 450))
        elif filename == 'data/level3.txt':
            # 7 на 7
            self.left = 100
            self.top = -20
            self.cell_size = 60
            draw_text('Уровень 3', (10, 450))

    def render(self):
        for i in range(self.width):
            for j in range(self.width):
                left = self.left + i * self.cell_size
                right = self.top + j * self.cell_size - i * self.cell_size
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


def start_screen():
    global LEVEL
    # fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    # screen.blit(fon, (0, 0))
    screen.fill(pygame.Color('#d5ffd9'))
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
    all_sprites = pygame.sprite.Group()
    Button(all_sprites, 0, "quit.png", (160, 520))
    Button(all_sprites, 'menu.png', 'menu.png', (8, 8))
    fon = pygame.transform.scale(load_image('fon_level.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    board = Board(LEVEL)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in all_sprites:
                    button.update(event)
                if LEVEL == 0:
                    return
                    # pos = pygame.mouse.get_pos()
            # pressed = pygame.mouse.get_pressed()
            # if pressed[0]:
            #    board.get_click(pos)
        # pressed = False
        board.render()
        all_sprites.draw(screen)
        pygame.display.flip()


while running:
    start_screen()
    game()
