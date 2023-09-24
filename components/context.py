import pygame
from components import fs, card

settings = fs.load("settings.json")["window"]


class Context:
    surface = None
    bg = None
    objects = []

    def __init__(self):
        self.set_up_window()

    def set_up_window(self):
        pygame.init()
        pygame.display.set_caption(settings["caption"])
        icon = pygame.image.load(settings["icon_path"])
        pygame.display.set_icon(icon)
        self.surface = pygame.display.set_mode((
            settings["width"],
            settings["height"]
        ))
        self.bg = pygame.Surface((
            settings["width"],
            settings["height"]
        ))
        self.bg.fill(pygame.Color(settings["background_color"]))

    def render_objects(self):
        self.surface.blit(self.bg, (0, 0))
        for i in self.objects:
            self.surface.blit(i.surface, i.position)
        pygame.display.update()

    def add_object(self, obj):
        self.objects.append(obj)
        self.render_objects()

    def run(self):
        is_running = True
        self.add_object(card.Card())

        while is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
