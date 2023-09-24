import pygame
from components import fs, card

settings = fs.load("settings.json")["window"]


class Context:
    surface = None

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
        bg = pygame.Surface((
            settings["width"],
            settings["height"]
        ))
        bg.fill(pygame.Color(settings["background_color"]))
        self.surface.blit(bg, (0, 0))

    def run(self):
        is_running = True
        test_blob = card.Card()
        self.surface.blit(test_blob.surface, (0, 0))
        pygame.display.update()
        while is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
