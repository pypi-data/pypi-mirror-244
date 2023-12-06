from .buttons import Button
import pygame
from os import path
from copy import deepcopy


class Game:
    execute = True
    width = 400
    height = 600
    diff = width / 3

    def __init__(self, grid):
        self.grid = grid
        self.initial_grid = deepcopy(grid)
        self.x = 1
        self.y = 1
        self.accepted_coords = list()
        self.current_coords = tuple()

    def __enter__(self):
        pygame.font.init()
        self.font1 = pygame.font.SysFont("comicsans", 75)
        self.font2 = pygame.font.SysFont("comicsans", 25)
        self.font3 = pygame.font.SysFont("comicsans", 35)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.events = EventHandler(self)
        self.buttons = pygame.sprite.Group()
        self.btn_restart = Button(self.screen, (90, 535), "Restart", 22, "black on skyblue", self.buttons)
        self.btn_next = Button(self.screen, (240, 535), "Next", 22, "white on gray", self.buttons)
        pygame.display.set_caption("Tic Tac Toe")
        self.load_icon()

    @staticmethod
    def load_icon():
        icon_path = path.join(path.dirname(path.abspath(__file__)), "icon.png")
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)

    def run(self):
        while self.execute:
            self.screen.fill((255, 255, 255))
            self.events.key_handler()
            self.draw()
            self.draw_box()
            self.buttons.update(self.screen)
            self.buttons.draw(self.screen)
            self.instruction()
            pygame.display.update()

    def get_cord(self, pos):
        self.x = pos[0] // self.diff
        self.y = pos[1] // self.diff

    def draw_box(self):
        for i in range(2):
            pygame.draw.line(self.screen, "skyblue4", (self.x * self.diff - 3, (self.y + i) * self.diff),
                             (self.x * self.diff + self.diff + 3, (self.y + i) * self.diff), 7)
            pygame.draw.line(self.screen, "skyblue4", ((self.x + i) * self.diff, self.y * self.diff),
                             ((self.x + i) * self.diff, self.y * self.diff + self.diff), 7)
            if self.grid.tiles[int(self.x)][int(self.y)].status is None:
                choice = self.font1.render(str("X" if self.grid.choice == "O" else "O"), 1, (211, 211, 211))
                self.screen.blit(choice, (self.x * self.diff + 36, self.y * self.diff + 7))

    def draw(self):
        for i in range(3):
            for j in range(3):
                if self.grid.tiles[i][j].status is not None:
                    text1 = self.font1.render(str(self.grid.tiles[i][j]), 1, (0, 0, 0))
                    self.screen.blit(text1, (i * self.diff + 36, j * self.diff + 7))

        for i in range(4):
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * self.diff), (self.width, i * self.diff), 1)
            pygame.draw.line(self.screen, (0, 0, 0), (i * self.diff, 0), (i * self.diff, self.width), 1)

    def instruction(self):
        if self.grid.winner:
            text1 = self.font3.render(self.grid.winner + " Won!", 1, "skyblue4")
            self.screen.blit(text1, (143, 410))
        elif self.grid.draw:
            text1 = self.font3.render("Draw!", 1, "skyblue4")
            self.screen.blit(text1, (143, 410))
        text2 = self.font2.render(f"X: {self.grid.x}", 1, "black")
        self.screen.blit(text2, (50, 465))
        text2 = self.font2.render(f"O: {self.grid.o}", 1, "black")
        self.screen.blit(text2, (300, 465))
        text2 = self.font2.render(f"Draw: {self.grid.d}", 1, "black")
        self.screen.blit(text2, (155, 465))

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pygame.quit()


class EventHandler:
    def __init__(self, game):
        self.game = game

    def key_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.execute = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.block_click()
                self.button_click()
            if event.type == pygame.KEYDOWN:
                self.keyboard_handler(event)
            if event.type == pygame.MOUSEMOTION:
                self.mouse_motion()

    def key_left(self):
        if self.game.x > 0:
            self.game.x -= 1

    def key_right(self):
        if self.game.x < 2:
            self.game.x += 1

    def key_up(self):
        if self.game.y > 0:
            self.game.y -= 1

    def key_down(self):
        if self.game.y < 2:
            self.game.y += 1

    def keyboard_handler(self, event):
        if event.key == pygame.K_LEFT:
            self.key_left()
        elif event.key == pygame.K_RIGHT:
            self.key_right()
        elif event.key == pygame.K_UP:
            self.key_up()
        elif event.key == pygame.K_DOWN:
            self.key_down()
        elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
            self.key_enter()

    def key_enter(self):
        self.game.btn_next.colors = "white on gray"
        if self.game.grid.winner or self.game.grid.draw:
            self.game.grid.restart()
        else:
            self.game.grid.insert((int(self.game.x), int(self.game.y)))
            if self.game.grid.winner or self.game.grid.draw:
                self.game.btn_next.colors = "black on skyblue"

    def block_click(self):
        pos = pygame.mouse.get_pos()
        if 0 <= pos[0] <= self.game.width and 0 <= pos[1] <= self.game.width:
            self.game.get_cord(pos)

    def button_click(self):
        if self.game.btn_next.rect.collidepoint(pygame.mouse.get_pos()):
            self.game.grid.restart()
        if self.game.btn_restart.rect.collidepoint(pygame.mouse.get_pos()):
            self.game.grid = deepcopy(self.game.initial_grid)

    def mouse_motion(self):
        if self.game.btn_next.rect.collidepoint(pygame.mouse.get_pos()):
            if self.game.grid.winner or self.game.grid.draw:
                self.game.btn_next.colors = "white on skyblue4"
            else:
                self.game.btn_next.colors = "white on gray"
        elif self.game.btn_restart.rect.collidepoint(pygame.mouse.get_pos()):
            self.game.btn_restart.colors = "white on skyblue4"
        else:
            self.game.btn_restart.colors = "black on skyblue"
            if self.game.grid.winner or self.game.grid.draw:
                self.game.btn_next.colors = "black on skyblue"
            else:
                self.game.btn_next.colors = "white on gray"