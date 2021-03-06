import pygame, sys, os


# очень нужные функции: для загрузки изображения и для написания текста
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


def terminate():
    pygame.quit()
    sys.exit()
    # стандартная функция выхода из программы


FPS = 50
pygame.init()
size = WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode(size)
fon_color = pygame.Color('#d5ffd9')
# единый цвет для всего фона в игре
shadow_color = pygame.Color('#a9f0b0')
# единый цвет всех кнопок
clock = pygame.time.Clock()
running = True
# существует для работы циклов
draw = False
WIN = False
# проверка победы
LEVEL = 0  # нужна, чтобы запомнить, какой уровень выбрал пользователь
CHANGE = None  # нужна, чтобы запомнить, какое дерево выбрал пользователь
COUNTER = 0  # счётчик ходов

# чтобы не загружать одно и то же изображение каждый раз, когда создаём клетку, используем библиотеку
tile_images = {'grass': load_image('grass.png'), 'tent': load_image('tent.png'),
               'none': load_image('gray.png'),
               'wrong_tent': load_image('wrong_tent.png')}

# чтобы не загружать одно и то же изображение каждый раз, когда меняем дерево, используем библиотеку
all_trees_images = {0: load_image('tree.png'), 1: load_image('tree_1.png'), 2: load_image('tree_2.png'),
                    3: load_image('tree_3.png'), 4: load_image('tree_4.png'), 5: load_image('tree_5.png'),
                    6: load_image('tree_6.png'), 7: load_image('tree_7.png'), 8: load_image('tree_8.png'),
                    9: load_image('tree_9.png'), 10: load_image('tree_10.png'), 11: load_image('tree_11.png'),
                    12: load_image('tree_12.png'), 13: load_image('tree_13.png'), 14: load_image('tree_14.png'),
                    15: load_image('tree_15.png'), 16: load_image('tree_16.png'), 17: load_image('tree_17.png'),
                    18: load_image('tree_18.png'), 19: load_image('tree_19.png')}

# чтобы не загружать одно и то же изображение каждый раз, когда создаём кнопку, используем библиотеку
all_buttons_images = {'menu.png': load_image('menu.png'),
                      'level1.txt': pygame.transform.scale(load_image("level1.png"), (110, 110)),
                      'level2.txt': pygame.transform.scale(load_image("level2.png"), (110, 110)),
                      'level3.txt': pygame.transform.scale(load_image("level3.png"), (110, 110)),
                      'level4.txt': pygame.transform.scale(load_image("level4.png"), (110, 110)),
                      'level5.txt': pygame.transform.scale(load_image("level5.png"), (110, 110)),
                      'level6.txt': pygame.transform.scale(load_image("level6.png"), (110, 110)),
                      'level7.txt': pygame.transform.scale(load_image("level7.png"), (110, 110)),
                      'level8.txt': pygame.transform.scale(load_image("level8.png"), (110, 110)),
                      'quit': load_image("quit.png")}


class Button(pygame.sprite.Sprite):
    def __init__(self, group, num, coor):
        super().__init__(group)
        self.num = num
        # переменная, необходимая, чтобы определить тип кнопки
        if self.num not in all_trees_images:
            self.image = all_buttons_images[self.num]
        else:
            self.image = all_trees_images[self.num]
        # по типу кнопки находим в библиотеке all_buttons_images соответствующее изображение
        sizes = self.image.get_size()
        # sizes нужно, чтобы тень была того же размера, что и изображение
        pygame.draw.rect(screen, shadow_color, (coor[0] + 10, coor[1] + 10, sizes[0], sizes[1]), 0)
        # рисуем тень
        self.rect = self.image.get_rect()
        self.rect.x = coor[0]
        self.rect.y = coor[1]

    def update(self, *args):
        global LEVEL, CHANGE
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            if self.num == 'quit':
                terminate()
                # при нажатии на кнопку "выйти из игры"
            elif self.num == 'menu.png':
                LEVEL = 0
                # при нажатии на кнопку выхода в меню, меняем глобальную переменную
                # см. строку 272-273
            elif self.num in ('level1.txt', 'level2.txt', 'level3.txt', 'level4.txt', 'level5.txt',
                              'level6.txt', 'level7.txt', 'level8.txt'):
                LEVEL = self.num
                # при нажатии на кнопку уровня, меняем глобальную переменную
                # см. строки 246-247
            elif self.num in all_trees_images:
                CHANGE = self.num


class Cell(pygame.sprite.Sprite):
    # клетка с деревом (не изменяется при нажатии)
    def __init__(self, group, image, coor):
        super().__init__(group)
        self.co = coor
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = coor[0] + 2.5
        self.rect.y = coor[1] + 2.5

    def check(self, *other):
        pass


class ActiveCell(pygame.sprite.Sprite):
    # пустая клетка/с травой/с палаткой (изменяется при нажатии)
    def __init__(self, group, coor, cell_size, num):
        super().__init__(group)
        self.co = coor
        self.cell_size = cell_size
        self.counter = 0
        # counter нужен, чтобы запомнить, что сейчас изображено в клетке
        self.sprites = [pygame.transform.scale(tile_images['none'], (self.cell_size - 3, self.cell_size - 3)),
                        pygame.transform.scale(tile_images['grass'], (self.cell_size - 3, self.cell_size - 3)),
                        pygame.transform.scale(tile_images['tent'], (self.cell_size - 10, self.cell_size - 10)), '.',
                        '#', '@',
                        pygame.transform.scale(tile_images['wrong_tent'], (self.cell_size - 3, self.cell_size - 3))]
        self.image = self.sprites[self.counter]
        self.rect = self.image.get_rect()
        self.rect.x = coor[0] + 2.5
        self.rect.y = coor[1] + 2.5
        self.num = num
        # координаты отличаются от coor на 2.5, чтобы не залезать на рамки
        self.i = num[1]
        self.j = num[2]
        self.board = num[0]
        # переменная num хранит в себе изменяемый список и положение клетки в нём

    def update(self, coor):
        global COUNTER
        # проверка на то, что нажатие попало на кнопку
        if self.co[0] <= coor[0] <= self.co[0] + self.cell_size and self.co[1] + \
                self.cell_size >= coor[1] >= self.co[1]:
            if self.counter == 2:
                self.counter = 0
            else:
                self.counter += 1
            self.board[self.i] = self.board[self.i][:self.j] + self.sprites[self.counter + 3] + self.board[self.i][
                                                                                                (self.j + 1):]
            self.image = self.sprites[self.counter]
            COUNTER += 1

    def check(self, board):
        # если у пользователя палатка, а в ответе не палатка заменяем image
        if self.board[self.i][self.j] == '@' and board[self.i][self.j] != '@':
            self.image = self.sprites[-1]


class Board:
    def __init__(self, filename, groups):
        self.cells = groups
        # нужен, чтобы менять дизайн деревьев
        filename = "data/" + filename
        with open(filename, 'r') as mapFile:
            self.board = [line.strip() for line in mapFile]
        # переносим уровень в список
        self.width = len(self.board[0])
        # используется для рисования таблицы
        self.copy = []
        for el in self.board:
            res = ''
            for symb in el:
                if symb == '!':
                    res += '!'
                else:
                    res += '.'
            self.copy.append(res)
        # копия нужна, чтобы при проверке сравнивать нынешнее поле и окончательный результат
        # далее индвидуальные параметры для каждого размера таблицы
        if filename == 'data/level1.txt':
            # 5 на 5
            self.levelname = 1
            self.left = 115
            self.top = -25
            self.cell_size = 75
        elif filename in ('data/level2.txt', 'data/level3.txt'):
            # 6 на 6
            if filename == 'data/level2.txt':
                self.levelname = 2
                self.left = 120
                self.top = -25
                self.cell_size = 65
            elif filename == 'data/level3.txt':
                self.levelname = 3
                self.left = 125
                self.top = -20
                self.cell_size = 65

        elif filename in ('data/level4.txt', 'data/level5.txt'):
            # 7 на 7
            if filename == 'data/level4.txt':
                self.levelname = 4
            elif filename == 'data/level5.txt':
                self.levelname = 5
            self.left = 100
            self.top = -20
            self.cell_size = 60

        elif filename in ('data/level6.txt', 'data/level7.txt'):
            # 8 на 8
            if filename == 'data/level6.txt':
                self.levelname = 6
            elif filename == 'data/level7.txt':
                self.levelname = 7
            self.left = 90
            self.top = -20
            self.cell_size = 55

        elif filename in ('data/level8.txt'):
            # 9 на 9
            self.levelname = 8
            self.left = 90
            self.top = -25
            self.cell_size = 50
        draw_text('Уровень {}'.format(self.levelname), (10, 450))
        draw_text('Количество ходов: ' + str(COUNTER), (10, 170))

    def render(self):
        global CHANGE
        for i in range(self.width):
            for j in range(self.width):
                # создаём таблицу, добавляем спрайты клеток
                left = self.left + i * self.cell_size
                right = self.top + j * self.cell_size - i * self.cell_size
                if self.board[i][j] == '!' and self.levelname not in (3, 4, 5, 6, 7):
                    # отдельный класс для дерева, отдельное оформление для разных размеров таблиц
                    Cell(self.cells,
                         pygame.transform.scale(all_trees_images[CHANGE], (self.cell_size - 3, self.cell_size - 3)),
                         (right + left + 25, left - 25))
                elif self.board[i][j] == '!' and (self.levelname in range(3, 8)):
                    Cell(self.cells,
                         pygame.transform.scale(all_trees_images[CHANGE], (self.cell_size - 3, self.cell_size - 3)),
                         (right + left + 20, left - 20))
                elif self.board[i][j] == '!' and (self.levelname == 8):
                    Cell(self.cells,
                         pygame.transform.scale(all_trees_images[CHANGE], (self.cell_size - 3, self.cell_size - 3)),
                         (right + left + 30, left - 30))
                else:
                    # отдельный класс для кликабельных клеток, отдельное оформление для разных размеров таблиц
                    if self.levelname not in (3, 4, 5, 6, 7):
                        ActiveCell(self.cells, (right + left + 25, left - 25), self.cell_size, (self.copy, i, j))
                    else:
                        ActiveCell(self.cells, (right + left + 20, left - 20), self.cell_size, (self.copy, i, j))
                # рисуем сетку
                pygame.draw.rect(screen, pygame.Color('black'), (left, right + left, self.cell_size, self.cell_size), 2)

        if self.levelname == 3:
            for i in range(len(self.board)):
                # пишем числа по вертикали (считаем палатки в каждом ряду)
                draw_text(str(self.board[i].count('@')),
                          (-5.9 * self.top + i * self.cell_size, self.left - self.cell_size + 25))
        elif self.levelname == 6 or self.levelname == 7:
            for i in range(len(self.board)):
                draw_text(str(self.board[i].count('@')),
                          (-4 * self.top + i * self.cell_size, self.left - self.cell_size + 35))
        elif self.levelname == 8:
            for i in range(len(self.board)):
                draw_text(str(self.board[i].count('@')),
                          (-3 * self.top + i * self.cell_size, self.left - self.cell_size + 20))
        else:
            for i in range(len(self.board)):
                draw_text(str(self.board[i].count('@')),
                          (-4.9 * self.top + i * self.cell_size, self.left - self.cell_size + 25))
        for j in range(len(self.board)):
            # пишем числа по горизонтали
            # counter нужен, чтобы пройтись по каждому столбцу
            counter = 0
            for i in range(len(self.board)):
                if self.board[i][j] == '@':
                    counter += 1
            if self.levelname == 3:
                draw_text(str(counter), (self.left - self.cell_size, -6 * self.top + j * self.cell_size + 30))
            elif self.levelname == 6 or self.levelname == 7:
                draw_text(str(counter), (self.left - self.cell_size, -6 * self.top + j * self.cell_size - 10))
            elif self.levelname == 8:
                draw_text(str(counter), (self.left - self.cell_size, -6 * self.top + j * self.cell_size - 42))
            else:
                draw_text(str(counter), (self.left - self.cell_size + 10, -5 * self.top + j * self.cell_size + 25))

    def get_cell(self, mouse_pos):
        for i in range(self.height):
            for j in range(self.width):
                if i <= (mouse_pos[1] + 30) // 30 <= i + 1 and j <= (mouse_pos[0] + 30) // 30 <= j + 1:
                    return j, i

    def get_click(self, mouse_pos):
        # принимаем нажатие и обновляем (?) каждую клетку
        for el in self.cells:
            el.update(mouse_pos)
        self.check()  # проводим проверку на победу
        self.cells.draw(screen)
        pygame.draw.rect(screen, fon_color, (165, 10, 275, 30), 0)
        draw_text('Количество ходов: ' + str(COUNTER), (10, 170))

    def check(self):
        # собственно, проверка на победу
        global WIN
        # переменная, чтобы при случае всё изменить и завершить уровень
        for el in self.cells:
            el.check(self.board)
        # проводим проверку в каждом спрайте
        if self.copy == self.board:
            WIN = True


def start_screen():
    global LEVEL
    # переменная LEVEL нужна, чтобы запомнить уровень, который будет открыт
    # глобальная она, потому что используется в функции game(), а в этой функции меняется
    # далее идёт создание изображения и текста
    screen.fill(fon_color)
    draw_text('Палатки', (50, 48), 58, 'red')
    draw_text('и', (50, 286), 58)
    draw_text('деревья', (50, 350), 58, '#00ce05')
    # специальный зелёный цвет
    # draw_text('made by maria andreeva', (570, 190), 22)
    # мне не понравилось, как выглядит подпись после добавления ещё пяти уровней
    rules = ['Вам нужно расположить по одной палатке рядом с ', 'каждым деревом. Она должна соприкасаться с ним по ',
             'вертикали или горизонтали. Цифры показывают число ', 'палаток в строке или колонке. Палатки не могут ',
             'соприкасаться даже по диагонали.']
    x = 120  # координата первой фразы
    for el in rules:
        draw_text(el, (x, 20), 23)
        x += 25
    sprites_start_screen = pygame.sprite.Group()
    Button(sprites_start_screen, 'level1.txt', (18, 260))
    Button(sprites_start_screen, 'level2.txt', (167, 260))
    Button(sprites_start_screen, 'level3.txt', (316, 260))
    Button(sprites_start_screen, 'level4.txt', (465, 260))
    Button(sprites_start_screen, 'level5.txt', (18, 390))
    Button(sprites_start_screen, 'level6.txt', (167, 390))
    Button(sprites_start_screen, 'level7.txt', (316, 390))
    Button(sprites_start_screen, 'level8.txt', (465, 390))
    Button(sprites_start_screen, 'quit', (160, 530))
    sprites_start_screen.draw(screen)
    # создаём и рисуем кнопки
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in sprites_start_screen:
                    button.update(event)
                if LEVEL != 0:
                    return
                # если после нажатия кнопки, переменная LEVEL изменилась, мы выходим из функции
                # как только функция перестаёт работать, начинает свою работу функция game()
        pygame.display.flip()
        clock.tick(FPS)


def change():
    global CHANGE
    screen.fill(fon_color)
    change_sprites = pygame.sprite.Group()
    draw_text('Выберите дерево', (50, 200))
    Button(change_sprites, 'quit', (160, 530))
    Button(change_sprites, 'menu.png', (8, 8))
    for i in range(5):
        Button(change_sprites, i, (110 + i * 80, 100))
    for i in range(5, 10):
        Button(change_sprites, i, (110 + (i - 5) * 80, 200))
    for i in range(10, 15):
        Button(change_sprites, i, (110 + (i - 10) * 80, 300))
    for i in range(15, 20):
        Button(change_sprites, i, (110 + (i - 15) * 80, 400))
    change_sprites.draw(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in change_sprites:
                    button.update(event)
                if LEVEL == 0:
                    return
                if CHANGE != None:
                    return
                # если переменная LEVEL изменилась (нажата кнопка "назад"), мы выходим из функции
                # цикл (268 строка) начинает свою работу повторно, с функции start_screen()
        pygame.display.flip()
        clock.tick(FPS)


def game():
    global LEVEL
    screen.fill(fon_color)
    all_sprites = pygame.sprite.Group()
    cells = pygame.sprite.Group()
    Button(all_sprites, 'quit', (160, 530))
    Button(all_sprites, 'menu.png', (8, 8))
    all_sprites.draw(screen)
    # создаём и рисуем кнопки
    board = Board(LEVEL, cells)
    board.render()
    # создаём и рисуем поле. какое - определяет переменная LEVEL
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in all_sprites:
                    button.update(event, board)
                if LEVEL == 0:
                    return
                    # если переменная LEVEL изменилась (нажата кнопка "назад"), мы выходим из функции
                    # цикл (268 строка) начинает свою работу повторно, с функции start_screen()
                if WIN:
                    return
                    # если переменная WIN изменилась (уровень пройден), мы выходим из функции
                    # сразу после этого начинает свою работу функция winner()
                pos = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0]:
                    board.get_click(pos)
            cells.draw(screen)
            pygame.display.flip()


def winner():
    global WIN
    screen.fill(fon_color)
    WIN = False
    draw_text('Вы победили!', (250, 130), 56)
    winner_sprites = pygame.sprite.Group()
    Button(winner_sprites, 'menu.png', (250, 320))
    winner_sprites.draw(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in winner_sprites:
                    button.update(event)
                if LEVEL == 0:
                    return
                # если переменная LEVEL изменилась (нажата кнопка "назад"), мы выходим из функции
                # цикл (268 строка) начинает свою работу повторно, с функции start_screen()
        pygame.display.flip()
        clock.tick(FPS)


while running:
    start_screen()
    # начальный экран с ссылками на три уровня
    CHANGE = None
    # меняем переменную перед запуском экрана выбора
    change()
    # экран выбора дерева
    game()
    # один из уровней
    if WIN:
        winner()
        # окно с поздравлением в случае победы
