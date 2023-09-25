import pygame
from components import fs, scale, animation

settings = fs.load("settings.json")["window"]
bg_color = settings["background_color"]


class Object:
    _x, _y = 0, 0
    target_x, target_y = 0, 0
    color = "#ff0000"
    scale = scale.Scale(scale.ScaleModes.INHERIT)
    width = scale.apply(100)
    height = scale.apply(100)

    def __init__(self):
        self.translate_anim = animation.Animation(
            lambda x: x / settings["translation_time"], settings["translation_time"],
            on_finished=self.hook_translate_finished
        )
        self.bg = pygame.Surface(self.dimensions)
        self.bg.fill(bg_color)
        self.surface = pygame.Surface(self.dimensions)
        self.draw()

    @property
    def x(self):
        if self.translate_anim:
            return self.translate_anim.value * (self.target_x - self._x) + self._x
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        if self.translate_anim:
            return self.translate_anim.value * (self.target_y - self._y) + self._y
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

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

    def translate(self, x, y):
        self.target_x = x
        self.target_y = y
        self.translate_anim.going_up = True

    def hook_translate_finished(self, anim_obj):
        self._x = self.target_x
        self._y = self.target_y
        anim_obj.reset()

    def is_inside(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.height

    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.rect)
