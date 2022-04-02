import pygame
import random

pygame.init()
pygame.display.set_caption("Измерение скорости пули с помощью баллистического маятника")
PISTOL = pygame.image.load('img/pistol.jpg')
PISTOL_STARTED = pygame.image.load("img/pistol_started.jpg")
START = pygame.image.load('img/start.png')
SMOKE = pygame.image.load("img/smoke.jpg")
EMPTY_ALLUMINIUM_BULLET = pygame.image.load("img/empty_alluminium.png")
ALLUMINIUM_BULLET = pygame.image.load("img/alluminium.png")
STEEL_BULLET = pygame.image.load("img/steel.png")
EMPTY_BRASS_BULLET = pygame.image.load("img/empty_brass.png")
BRASS_BULLET = pygame.image.load("img/brass.png")
ALTMARK = pygame.image.load("img/altmark.jpg")
INFO = pygame.image.load("img/info.png")
ICON = pygame.image.load("img/icon.png")

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
                    if 1200 < pos[0] < 1280 and 530 < pos[1] < 600 and not self.started:
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
            self.clock.tick(60)
            self.render()
            pygame.display.flip()

    def render(self):
        self.screen.fill(pygame.Color("White"))
        # Установка
        pygame.draw.line(self.screen, pygame.Color('black'), (250, 120), (700, 120), width=5)
        pygame.draw.line(self.screen, pygame.Color('black'), (550, 120),
                         (self.ticker.left + self.ticker.width - 50, self.ticker.top), width=2)
        pygame.draw.line(self.screen, pygame.Color('black'), (400, 120), (self.ticker.left + 50, self.ticker.top),
                         width=2)
        pygame.draw.rect(self.screen, pygame.Color('black'), self.ticker.rect(), width=0)
        # Кнопки
        self.screen.blit(START, (1200, 530))
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
            self.screen.blit(SMOKE, (self.pistol.coords[0] - 15, self.pistol.coords[1] - 100))
        else:
            self.screen.blit(PISTOL, self.pistol.coords)
        pygame.draw.line(self.screen, pygame.Color("black"), (self.pistol.coords[0], self.pistol.coords[1] + 65),
                         (self.pistol.coords[0] + 100, self.pistol.coords[1] + 65),
                         width=2)
        # Угол отклонения
        font = pygame.font.SysFont("comicsansms", 30)
        text = font.render(f"α = {str(self.angle)}", True, pygame.Color("Black"))
        self.screen.blit(text, (500, 500))
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
        current_bullet_coords = [self.coords[0] + 20, self.coords[1] + 20]
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
            return True
        return False

    def move(self):
        self.coords[0] -= self.velocity / FPS


class Ticker():
    def __init__(self, coords, bullet):
        self.left = coords[0]
        self.top = coords[1]
        self.width = coords[2]
        self.height = coords[3]
        self.weight = 0
        self.velocity = 50
        self.y_velocity = 1
        self.acceleration = 10
        if bullet == 0:
            self.velocity = 130
            self.y_velocity = 1
        elif bullet == 1:
            self.velocity = 160
            self.y_velocity = 1.5
        elif bullet == 2:
            self.velocity = 320
            self.y_velocity = 3
        elif bullet == 3:
            self.velocity = 330
            self.y_velocity = 3
        elif bullet == 4:
            self.velocity = 350
            self.y_velocity = 4
        else:
            self.velocity = 500

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
        self.velocity -= self.acceleration
        if self.velocity < 0:
            self.velocity = 0

    def move(self):
        self.update_velocity()
        self.left -= self.velocity / FPS
        self.top -= self.y_velocity / FPS


lab = Lab()
lab.run()
