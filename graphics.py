import pygame
from card import *
from random import shuffle

WINDOW_NAME = "Solitaire"
WINDOW_SIZE = (1200, 800)
BACKGROUND_COLOR = "#037d02"


class GameCard(Card):
    def __init__(
        self,
        suit: Suit,
        value: Value,
        surface: pygame.Surface,
    ):
        super().__init__(suit, value)
        self.x = 0
        self.y = 0
        self.width = 110
        self.height = 160
        self.factor = 1.0
        self.surface = surface
        self.cache = {}
        self.stack = None
        self.is_covered = False
        self.dragged = False
        self.drag_start = (0, 0)
        self.drag_lead = False
        self.last_drag_pos = (0, 0)

    def moveTo(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def moveBy(self, x: float, y: float) -> None:
        self.x += x
        self.y += y

    def draw_cover(self) -> None:
        color = (252, 255, 252)
        border_size = 2 * self.factor
        border_color = (0, 0, 0)

        pygame.draw.rect(
            self.surface,
            border_color,
            pygame.Rect(
                self.x - border_size,
                self.y - border_size,
                (self.width + 2 * border_size) * self.factor,
                (self.height + 2 * border_size) * self.factor,
            ),
        )
        pygame.draw.rect(
            self.surface,
            color,
            pygame.Rect(
                self.x, self.y, self.width * self.factor, self.height * self.factor
            ),
        )

    def draw_text(self) -> None:
        font_size = int(28 * self.factor)
        suit_font_size = int(54 * self.factor)
        x_padding = 2 * self.factor
        y_padding = 5 * self.factor

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

    def draw_covered(self) -> None:
        color = (63, 134, 155)
        border_size = int(2 * self.factor)
        border_color = (0, 0, 0)
        cover_color = (42, 106, 128)
        block_size = 5
        row_skip = 25
        initial_margin = 14

        pygame.draw.rect(
            self.surface,
            border_color,
            pygame.Rect(
                self.x - border_size,
                self.y - border_size,
                (self.width + 2 * border_size) * self.factor,
                (self.height + 2 * border_size) * self.factor,
            ),
        )
        pygame.draw.rect(
            self.surface,
            color,
            pygame.Rect(
                self.x, self.y, self.width * self.factor, self.height * self.factor
            ),
        )

        for y_row in range(
            self.y + initial_margin,
            int(self.height * self.factor) + self.y - border_size,
            row_skip,
        ):
            for i, x_col in enumerate(
                range(
                    self.x,
                    int(self.width * self.factor) + self.x - border_size,
                    block_size,
                )
            ):
                pygame.draw.rect(
                    self.surface,
                    cover_color,
                    pygame.Rect(
                        x_col,
                        y_row + (block_size if i % 2 == 0 else 0),
                        block_size,
                        block_size,
                    ),
                )

    def render(self) -> None:
        if self.is_covered:
            self.draw_covered()
            return

        self.draw_cover()
        self.draw_text()

    @staticmethod
    def check_basic_hit(pos: tuple[int, int], card):
        return card.x <= pos[0] <= card.x + int(
            card.width * card.factor
        ) and card.y <= pos[1] <= card.y + int(card.height * card.factor)

    def check_hit(self, pos: tuple[int, int]) -> bool:
        if not self.check_basic_hit(pos, self):
            return False

        for i in reversed(self.stack):
            if self.check_basic_hit(pos, i):
                return i is self

    def mouse_down_event(self, mouse_pos: tuple[int, int]) -> None:
        if self.is_covered:
            return

        if not self.check_hit(mouse_pos):
            return

        self.drag_start = (self.x, self.y)
        self.dragged = True
        self.drag_lead = True
        self.last_drag_pos = mouse_pos
        found_self = False

        for i in self.stack:
            if found_self:
                i.drag_start = (i.x, i.y)
                i.dragged = True
                i.last_drag_pos = mouse_pos

            if i is self:
                found_self = True

    def mouse_up_event(self, mouse_pos: tuple[int, int]) -> None:
        if self.dragged:
            self.x, self.y = self.drag_start
            self.drag_lead = False
            self.dragged = False

    def apply_movement(self, mouse_pos: tuple[int, int] = (0, 0)) -> None:
        if self.dragged:
            self.x += mouse_pos[0] - self.last_drag_pos[0]
            self.y += mouse_pos[1] - self.last_drag_pos[1]
            self.last_drag_pos = mouse_pos

        if self.drag_lead:
            center_x = self.x + int(self.width * self.factor / 2)
            center_y = self.y + int(self.height * self.factor / 2)

    def mainloop(self, mouse_pos: tuple[int, int] = (0, 0)) -> None:
        self.apply_movement(mouse_pos)
        self.render()


class GameDeck(Deck):
    def __init__(self, surface: pygame.Surface, cards: list[GameCard] = None):
        self.surface = surface
        if cards:
            self._deck = cards
            return
        self._deck = []
        self.fill()

    def fill(self):
        for suit in range(SUITS):
            for values in range(VALUES):
                self._deck.append(GameCard(suit, values, self.surface))
        shuffle(self._deck)


def start() -> (pygame.Surface, pygame.Surface):
    pygame.init()
    pygame.display.set_caption(WINDOW_NAME)
    surface = pygame.display.set_mode(WINDOW_SIZE)
    background = pygame.Surface(WINDOW_SIZE)
    background.fill(pygame.Color(BACKGROUND_COLOR))
    return surface, background


is_running = True
surface, background = start()

deck = GameDeck(surface)
stacks = get_stacks(deck, True)

for stack_index, stack in enumerate(stacks):
    for card_index, card in enumerate(stack):
        card.moveTo(stack_index * 150 + 50, card_index * 40 + 50)
        if not card_index == len(stack) - 1:
            card.is_covered = True

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for stack in stacks:
                for card in stack:
                    card.mouse_down_event(pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONUP:
            for stack in stacks:
                for card in stack:
                    card.mouse_up_event(pygame.mouse.get_pos())

    surface.blit(background, (0, 0))
    late_render = []

    for stack in stacks:
        for card in stack:
            if card.dragged:
                late_render.append(card)
                continue
            card.mainloop(mouse_pos=pygame.mouse.get_pos())

    for card in late_render:
        card.mainloop(mouse_pos=pygame.mouse.get_pos())

    pygame.display.update()
