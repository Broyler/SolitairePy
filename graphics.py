import pygame
from card import *

WINDOW_NAME = "Solitaire"
WINDOW_SIZE = (1200, 800)
BACKGROUND_COLOR = "#037d02"


class GameCard(Card):
    def __init__(self, suit: Suit, value: Value, surface: pygame.Surface):
        super().__init__(suit, value)
        self.x = 0
        self.y = 0
        self.width = 110
        self.height = 160
        self.surface = surface
        self.cache = {}

    def moveTo(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def moveBy(self, x: float, y: float) -> None:
        self.x += x
        self.y += y

    def draw_cover(self) -> None:
        color = (252, 255, 252)
        border_size = 2
        border_color = (0, 0, 0)

        pygame.draw.rect(
            self.surface,
            border_color,
            pygame.Rect(
                self.x - border_size,
                self.y - border_size,
                self.width + 2 * border_size,
                self.height + 2 * border_size,
            ),
        )
        pygame.draw.rect(
            surface,
            color,
            pygame.Rect(self.x, self.y, self.width, self.height),
        )

    def draw_text(self) -> None:
        font_size = 28
        suit_font_size = 54
        x_padding = 2
        y_padding = 5

        img = self.cache.get("value_img")
        flipped_img = self.cache.get("flipped_value_img")
        suit_img = self.cache.get("suit_img")

        if not (img and flipped_img and suit_img):
            vcr_font = pygame.font.Font("font_vcr.ttf", font_size)
            suit_font = pygame.font.Font("font_vcr.ttf", suit_font_size)
            font_color = self.card_color()
            img = vcr_font.render(self.true_value(), True, font_color)
            flipped_img = pygame.transform.flip(img, True, True)
            suit_img = suit_font.render(self.suit_symbol(), True, font_color)
            self.cache.update(
                {
                    "value_img": img,
                    "flipped_value_img": flipped_img,
                    "suit_img": suit_img,
                }
            )

        self.surface.blit(img, (self.x + x_padding, self.y + y_padding))
        self.surface.blit(
            flipped_img,
            (
                self.x + self.width - 2 * x_padding - flipped_img.get_width(),
                self.y + self.height - y_padding - flipped_img.get_height(),
            ),
        )
        self.surface.blit(
            suit_img,
            (
                self.x + (self.width - suit_img.get_width()) / 2,
                self.y + (self.height - suit_img.get_height()) / 2,
            ),
        )

    def render(self) -> None:
        self.draw_cover()
        self.draw_text()


def start() -> (pygame.Surface, pygame.Surface):
    pygame.init()
    pygame.display.set_caption(WINDOW_NAME)
    surface = pygame.display.set_mode(WINDOW_SIZE)
    background = pygame.Surface(WINDOW_SIZE)
    background.fill(pygame.Color(BACKGROUND_COLOR))
    return surface, background


is_running = True
surface, background = start()

deck = Deck()
five_slice = Deck(deck.deck[0:7])
nd = []

for index, i in enumerate(five_slice.deck):
    a = GameCard(i._suit, i._value, surface)
    a.moveTo(50 + 120 * index, 100)
    nd.append(a)

nd.append(GameCard(Suit.CLUB, Value.KING, surface))
nd[-1].moveTo(50, 140)


while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    surface.blit(background, (0, 0))

    for i in nd:
        i.render()

    pygame.display.update()
