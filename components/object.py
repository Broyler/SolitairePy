import pygame
from components import fs, scale

settings = fs.load("settings.json")["window"]
bg_color = settings["background_color"]


class Object:
    x, y = 0, 0
    color = "#ff0000"
    scale = scale.Scale(scale.ScaleModes.INHERIT)
    width = scale.apply(100)
    height = scale.apply(100)

    def __init__(self):
        self.bg = pygame.Surface(self.dimensions)
        self.bg.fill(bg_color)
        self.surface = pygame.Surface(self.dimensions)
        self.draw()

    @property
    def position(self):
        return self.x, self.y

    @property
    def dimensions(self):
        return self.width, self.height

    @property
    def rect(self):
        return *self.position, *self.dimensions

    def inset_rect(self, padding):
        return self.x + padding, self.y + padding, self.width - 2 * padding, self.height - 2 * padding

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def move_by(self, delta_x, delta_y):
        self.x += delta_x
        self.y += delta_y

    def is_inside(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.height

    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.rect)
