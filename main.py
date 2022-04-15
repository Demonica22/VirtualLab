import pygame
import random

pygame.init()
pygame.display.set_caption("Измерение скорости пули с помощью баллистического маятника")
PISTOL = pygame.image.load('img/pistol.png')
PISTOL_STARTED = pygame.image.load('img/pistol_started.png')
START = pygame.image.load('img/start.png')
RESET = pygame.image.load('img/reset.png')
RULLER = pygame.image.load('img/ruler.png')
EMPTY_ALLUMINIUM_BULLET = pygame.image.load("img/empty_alluminium.png")
ALLUMINIUM_BULLET = pygame.image.load("img/alluminium.png")
STEEL_BULLET = pygame.image.load("img/steel.png")
EMPTY_BRASS_BULLET = pygame.image.load("img/empty_brass.png")
BRASS_BULLET = pygame.image.load("img/brass.png")
# ALTMARK = pygame.image.load("img/altmark.jpg")
INFO = pygame.image.load("img/info.png")
ICON = pygame.image.load("img/icon.png")
TICKER = pygame.image.load("img/ticker.png")
bullet_coords = [(700, 2), (810, 2), (920, 2), (1030, 9), (1140, 2)]
bullet_weights = [5.2, 6.8, 13.6, 13.8, 19, 9]
bullet_colors = ["grey", "blue", "black", "orange", "red"]
deltas = [(1295, 1305, 5), (1275, 1285, 5), (1170, 1190, 5), (1165, 1185, 5), (1100, 1120, 5)]
ticker_coords = (350, 300, 250, 100)

FPS = 60

pygame.display.set_icon(ICON)


class Lab:
    def __init__(self):
        self.doing = True
        self.started = False
        self.set_warning_message_bullet = False
        self.set_warning_message_ticker = False
        self.bullet_chosen = None
        self.screen = pygame.display.set_mode((1280, 600))
        self.screen.fill(pygame.Color("White"))
        self.clock = pygame.time.Clock()
        self.ticker = Ticker(ticker_coords, self.bullet_chosen)
        self.pistol = Pistol(self.ticker.get_coords())
        self.delta_x = 0

    def run(self):
        self.render()
        while self.doing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.doing = False
                # Обработка нажатий мыши
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    # Нажатие кнопки Старт
                    if 1180 < pos[0] < 1280 and 550 < pos[1] < 600 and not self.started:
                        if self.ticker.get_coords() != ticker_coords:
                            self.set_warning_message_ticker = True
                        else:
                            self.set_warning_message_ticker = False
                            self.start()
                    # Нажатие кнопки Сброс
                    if 1070 < pos[0] < 1170 and 550 < pos[1] < 600:
                        self.ticker.return_to_start_position()
                        self.started = False
                    # Нажатие на одну из иконок пуль
                    if not self.started:
                        for bullet in bullet_coords:
                            if bullet[0] <= pos[0] <= bullet[0] + 105 and bullet[1] <= pos[1] <= bullet[1] + 100:
                                self.bullet_chosen = bullet_coords.index(bullet)
                                self.set_warning_message_bullet = False
            if self.started:
                # Движение пули
                if not self.pistol.bullet.collide(self.ticker) and self.ticker.velocity > 0:
                    self.pistol.bullet.move()
                else:
                    # Движение бруска
                    self.ticker.move()
                    self.pistol.bullet.coords = [self.ticker.left + self.ticker.width, self.pistol.bullet.coords[1]]
                if self.ticker.reached_most_left_point and self.delta_x == 0:
                    #Генерация максимального отклонения бруска
                    self.delta_x = random.randrange(*deltas[self.bullet_chosen]) / 100
                if self.ticker.velocity == 0 and self.ticker.start_velocity == 0:
                    self.started = False
            self.clock.tick(60)
            self.render()
            pygame.display.flip()

    def render(self):
        self.screen.fill(pygame.Color("White"))
        # Установка
        self.screen.blit(RULLER, (-5, ticker_coords[1] + ticker_coords[3]))
        # Подвес и нити
        pygame.draw.line(self.screen, pygame.Color('black'), (250, 120), (695, 120), width=7)
        pygame.draw.line(self.screen, pygame.Color('black'), (550, 120),
                         (self.ticker.left + self.ticker.width - 50, self.ticker.top), width=2)
        pygame.draw.line(self.screen, pygame.Color('black'), (400, 120), (self.ticker.left + 50, self.ticker.top),
                         width=2)
        # Маятник
        self.screen.blit(TICKER, self.ticker.get_coords()[:2])
        # Подставка пистолета
        pygame.draw.line(self.screen, pygame.Color("black"), (800, 394), (899, 394), width=10)
        pygame.draw.rect(self.screen, pygame.Color("black"), pygame.Rect((850, 394), (5, 206)))
        pygame.draw.line(self.screen, pygame.Color("black"), (800, 598), (899, 598), width=10)

        # Кнопки
        self.screen.blit(START, (1180, 550))
        self.screen.blit(RESET, (1070, 550))
        # Пули
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
        if self.delta_x != 0:
            font = pygame.font.SysFont("comicsansms", 30)
            text = font.render(f"z = {str(self.delta_x)} см", True, pygame.Color("Black"))
            self.screen.blit(text, (300, 500))
        # Предупреждение о невыбранной пуле
        if self.set_warning_message_bullet:
            font = pygame.font.SysFont("comicsansms", 20)
            text = font.render(f"Выберите пулю!", True, pygame.Color("red"))
            self.screen.blit(text, (1000, 510))
        elif self.set_warning_message_ticker:
            font = pygame.font.SysFont("comicsansms", 15)
            print(self.ticker.get_coords())
            text = font.render("Маятник не на исходной", True, pygame.Color("red"))
            self.screen.blit(text, (1000, 510))
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
            self.delta_x = 0
            self.pistol.shoot()
        else:
            self.set_warning_message_bullet = True


class Pistol():
    def __init__(self, ticker_coords):
        self.coords = (ticker_coords[0] + ticker_coords[2] + 200, ticker_coords[1] + (ticker_coords[3] / 4))

    def shoot(self):
        self.bullet = Bullet([self.coords[0] + 5, self.coords[1] + 10])


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
        self.left = coords[0]
        self.top = coords[1]
        self.width = coords[2]
        self.height = coords[3]
        self.acceleration = 10
        self.velocity = 0
        if bullet == 0:
            self.velocity = 240
        elif bullet == 1:
            self.velocity = 250
        elif bullet == 2:
            self.velocity = 300
        elif bullet == 3:
            self.velocity = 305
        elif bullet == 4:
            self.velocity = 330
        self.start_velocity = self.velocity
        self.reached_most_left_point = False
    def set_coords(self, coords):
        self.left = coords[0]
        self.top = coords[1]

    def return_to_start_position(self):
        self.set_coords(ticker_coords[:2])
        self.velocity = 0
        self.acceleration = 0
        self.start_velocity = 0

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
        #print(self.velocity, self.start_velocity, self.acceleration)
        self.velocity -= self.acceleration
        if (self.velocity < 0 and self.acceleration > 0) or (self.velocity > 0 and self.acceleration < 0):
            self.velocity = 0
        if self.velocity == 0:
            if self.acceleration == 10:
                self.reached_most_left_point = True
                self.acceleration = 5
            self.start_velocity *= -0.85
            self.velocity = self.start_velocity
            self.acceleration *= -1
            if abs(self.start_velocity) < 15:
                self.return_to_start_position()
                self.start_velocity = 0
                self.acceleration = 0

    def move(self):
        self.update_velocity()
        self.left -= self.velocity / FPS


lab = Lab()
lab.run()
