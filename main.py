import pygame
import random
import time

pygame.init()
pygame.display.set_caption("Измерение скорости пули с помощью баллистического маятника")
PISTOL = pygame.image.load('img/pistol.png')
PISTOL_STARTED = pygame.image.load('img/pistol_started.png')
START = pygame.image.load('img/start.png')
PROTRACTOR = pygame.image.load("img/transportir.png")
EMPTY_ALLUMINIUM_BULLET = pygame.image.load("img/empty_alluminium.png")
ALLUMINIUM_BULLET = pygame.image.load("img/alluminium.png")
STEEL_BULLET = pygame.image.load("img/steel.png")
EMPTY_BRASS_BULLET = pygame.image.load("img/empty_brass.png")
BRASS_BULLET = pygame.image.load("img/brass.png")
ALTMARK = pygame.image.load("img/altmark.jpg")
INFO = pygame.image.load("img/info.png")
ICON = pygame.image.load("img/icon.png")
TICKER = pygame.image.load("img/ticker.png")
bullet_coords = [(700, 2), (810, 2), (920, 2), (1030, 9), (1140, 2)]
bullet_weights = [5.2, 6.8, 13.6, 13.8, 19, 9]
bullet_colors = ["grey", "blue", "black", "orange", "red"]
angles = [(195, 220, 1), (235, 250, 1), (325, 350, 1), (325, 350, 1), (375, 400, 1)]
ticker_coords = (350, 300, 250, 100)

FPS = 60

pygame.display.set_icon(ICON)


class Lab:
    def __init__(self):
        self.doing = True
        self.started = False
        self.set_warning_message = False
        self.bullet_chosen = None
        self.screen = pygame.display.set_mode((1280, 600))
        self.screen.fill(pygame.Color("White"))
        self.clock = pygame.time.Clock()
        self.ticker = Ticker(ticker_coords, self.bullet_chosen)
        self.pistol = Pistol(self.ticker.get_coords())
        self.angle = 0

    def run(self):
        self.render()
        while self.doing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.doing = False
                # Обработка нажатий мыши
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    # Нажатие кнопки Start
                    if 1180 < pos[0] < 1280 and 550 < pos[1] < 600 and not self.started:
                        self.start()
                    # Нажатие на одну из иконок пуль
                    for bullet in bullet_coords:
                        if bullet[0] <= pos[0] <= bullet[0] + 105 and bullet[1] <= pos[1] <= bullet[1] + 100:
                            self.bullet_chosen = bullet_coords.index(bullet)
                            self.set_warning_message = False
            if self.started:
                # Движение пули
                if not self.pistol.bullet.collide(self.ticker) and self.ticker.velocity > 0:
                    self.pistol.bullet.move()
                else:
                    # Движение бруска
                    self.ticker.move()
                    self.pistol.bullet.coords = [self.ticker.left + self.ticker.width, self.pistol.bullet.coords[1]]
                if self.ticker.velocity == 0:
                    # Генерация угла отклонения бруска
                    self.angle = random.randrange(*angles[self.bullet_chosen]) / 10
                    self.started = False
            if self.ticker.time is not None:
                if abs(int(self.ticker.time) - int(time.strftime("%S", time.gmtime()))) > 5:

                    left, top, width, height = self.ticker.get_coords()
                    if left < ticker_coords[0]:
                        if (abs(ticker_coords[0] - left) / FPS) > 0.01:
                            left += abs(ticker_coords[0] - left) / FPS
                        else:
                            left = ticker_coords[0]

                    if top < ticker_coords[1]:
                        if (abs(ticker_coords[1] - top) / FPS) > 0.01:
                            top += abs(ticker_coords[1] - top) / FPS
                        else:
                            top = ticker_coords[1]
                    self.ticker.set_coords((left, top))
            self.clock.tick(60)
            self.render()
            pygame.display.flip()

    def render(self):
        self.screen.fill(pygame.Color("White"))
        # Установка
        pygame.draw.line(self.screen, pygame.Color('black'), (250, 120), (700, 120), width=5)
        self.screen.blit(PROTRACTOR, (300, 125))
        pygame.draw.line(self.screen, pygame.Color('black'), (550, 120),
                         (self.ticker.left + self.ticker.width - 50, self.ticker.top), width=2)
        pygame.draw.line(self.screen, pygame.Color('black'), (400, 120), (self.ticker.left + 50, self.ticker.top),
                         width=2)
        self.screen.blit(TICKER, self.ticker.get_coords()[:2])
        # Кнопки
        self.screen.blit(START, (1180, 550))
        self.screen.blit(EMPTY_ALLUMINIUM_BULLET, bullet_coords[0])
        self.screen.blit(ALLUMINIUM_BULLET, bullet_coords[1])
        self.screen.blit(STEEL_BULLET, bullet_coords[2])
        self.screen.blit(EMPTY_BRASS_BULLET, bullet_coords[3])
        self.screen.blit(BRASS_BULLET, bullet_coords[4])
        if self.bullet_chosen is not None:
            pygame.draw.rect(self.screen, pygame.Color('red'),
                             pygame.Rect((bullet_coords[self.bullet_chosen][0], 0), (100, 100)), width=3)
        # Информация об установке
        self.screen.blit(INFO, (0, 0))
        # Пистолет
        if self.started:
            self.screen.blit(PISTOL_STARTED, self.pistol.coords)
        else:
            self.screen.blit(PISTOL, self.pistol.coords)
        # Угол отклонения
        if self.angle != 0:
            font = pygame.font.SysFont("comicsansms", 30)
            text = font.render(f"α = {str(self.angle)}°", True, pygame.Color("Black"))
            self.screen.blit(text, (300, 500))
        # Предупреждение о невыбранной пуле
        if self.set_warning_message:
            font = pygame.font.SysFont("comicsansms", 20)
            text = font.render(f"Выберите пулю!", True, pygame.Color("red"))
            self.screen.blit(text, (1000, 545))
        # Пуля
        if self.started:
            pygame.draw.circle(self.screen, pygame.Color(bullet_colors[self.bullet_chosen]), self.pistol.bullet.coords,
                               self.pistol.bullet.radius)
        pygame.display.flip()

    def start(self):
        if self.bullet_chosen is not None:
            # Создание экземпляров пули и бруска для текущего высрела и сам выстрел
            self.ticker = Ticker(ticker_coords, self.bullet_chosen)
            self.pistol = Pistol(self.ticker.get_coords())
            self.started = True
            self.angle = 0
            self.pistol.shoot()
        else:
            self.set_warning_message = True


class Pistol():
    def __init__(self, ticker_coords):
        self.coords = (ticker_coords[0] + ticker_coords[2] + 200, ticker_coords[1] + (ticker_coords[3] / 4))

    def shoot(self):
        current_bullet_coords = [self.coords[0] + 5, self.coords[1] + 10]
        self.bullet = Bullet(current_bullet_coords)


class Bullet():
    def __init__(self, coords):
        self.coords = coords
        self.radius = 6  # Радиус шарика на экране
        self.velocity = 500  # Скорость шарика на экране

    def collide(self, ticker):
        """
        Проверка на пересечение пули и бруска
        :param ticker:
        :return: Bool
        """
        if ticker.left <= self.coords[0] <= ticker.left + ticker.width and ticker.top <= self.coords[
            1] <= ticker.top + ticker.height:
            self.coords[0] = ticker.left + ticker.width
            self.coords[1] = ticker.top + ticker.height / 4 + 10
            return True
        return False

    def move(self):
        self.coords[0] -= self.velocity / FPS


class Ticker():
    def __init__(self, coords, bullet):
        self.time = None
        self.left = coords[0]
        self.top = coords[1]
        self.width = coords[2]
        self.height = coords[3]
        self.weight = 0
        self.velocity = 50
        self.y_velocity = 1
        self.acceleration = 10
        if bullet == 0:
            self.velocity = 290
            self.y_velocity = 10
        elif bullet == 1:
            self.velocity = 300
            self.y_velocity = 10
        elif bullet == 2:
            self.velocity = 370
            self.y_velocity = 15
        elif bullet == 3:
            self.velocity = 370
            self.y_velocity = 14
        elif bullet == 4:
            self.velocity = 390
            self.y_velocity = 20

    def set_coords(self, coords):
        self.left = coords[0]
        self.top = coords[1]

    def rect(self):
        """
        Возвращает объект прямоугольника текущекого маятника
        :return: Rect
        """
        return pygame.Rect(self.left, self.top, self.width, self.height)

    def get_coords(self):
        """
        Возвращает координаты левого верхнего угла, ширину и высоту
        :return: tuple
        """
        return self.left, self.top, self.width, self.height

    def update_velocity(self):
        if self.time is None:
            self.time = time.strftime("%S", time.gmtime())
        self.velocity -= self.acceleration
        if self.velocity < 0:
            self.velocity = 0

    def move(self):
        self.update_velocity()
        self.left -= self.velocity / FPS
        self.top -= self.y_velocity / FPS


lab = Lab()
lab.run()
