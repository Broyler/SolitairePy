import pygame
from card import *
from random import shuffle
from math import ceil

WINDOW_NAME = "Solitaire"
WINDOW_SIZE = (1200, 800)
BACKGROUND_COLOR = "#037d02"
RENDER_FACTOR = 0.8
CARD_WIDTH = round(110 * RENDER_FACTOR)
CARD_HEIGHT = round(160 * RENDER_FACTOR)
HORIZONTAL_SPACING = round(CARD_WIDTH * 1.2)
VERTICAL_SPACING = round(CARD_HEIGHT * 0.25)
CORNER_PADDING = round(50 * RENDER_FACTOR)


class GameCard(Card):
    def __init__(
        self,
        suit: Suit,
        value: Value,
        surface: pygame.Surface,
        is_static: bool = False,
        all_draw: list = [],
        now_draw: list = [],
    ):
        super().__init__(suit, value)
        self.is_static = is_static
        self.x = 0
        self.y = 0
        self.surface = surface
        self.cache = {}
        self.stack = []
        self.total_draw_stack = all_draw
        self.uncovered_draw_stack = now_draw
        self.click_start_static = False
        self.all_stacks = []
        self.is_covered = False
        self.click_pos = (0, 0)
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
        border_size = ceil(2 * RENDER_FACTOR)
        border_color = (0, 0, 0)

        pygame.draw.rect(
            self.surface,
            color,
            pygame.Rect(self.x, self.y, CARD_WIDTH, CARD_HEIGHT),
        )
        pygame.draw.rect(
            self.surface,
            border_color,
            pygame.Rect(
                self.x - border_size,
                self.y - border_size,
                round(CARD_WIDTH + 2 * border_size),
                round(CARD_HEIGHT + 2 * border_size),
            ),
            border_size,
        )

    def draw_text(self) -> None:
        font_size = round(28 * RENDER_FACTOR)
        suit_font_size = round(54 * RENDER_FACTOR)
        x_padding = 2 * RENDER_FACTOR
        y_padding = 5 * RENDER_FACTOR

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
                self.x + CARD_WIDTH - 2 * x_padding - flipped_img.get_width(),
                self.y + CARD_HEIGHT - y_padding - flipped_img.get_height(),
            ),
        )
        self.surface.blit(
            suit_img,
            (
                self.x + (CARD_WIDTH - suit_img.get_width()) / 2,
                self.y + (CARD_HEIGHT - suit_img.get_height()) / 2,
            ),
        )

    def draw_covered(self) -> None:
        color = (63, 134, 155)
        border_size = ceil(2 * RENDER_FACTOR)
        border_color = (0, 0, 0)
        cover_color = (42, 106, 128)
        block_size = ceil(5 * RENDER_FACTOR)
        row_skip = round(25 * RENDER_FACTOR)
        initial_margin = round(14 * RENDER_FACTOR)

        pygame.draw.rect(
            self.surface,
            color,
            pygame.Rect(self.x, self.y, CARD_WIDTH, CARD_HEIGHT),
        )

        for y_row in range(
            self.y + initial_margin,
            self.y + CARD_HEIGHT - border_size,
            row_skip,
        ):
            for i, x_col in enumerate(
                range(
                    self.x,
                    CARD_WIDTH + self.x - border_size,
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

        pygame.draw.rect(
            self.surface,
            border_color,
            pygame.Rect(
                self.x - border_size,
                self.y - border_size,
                round(CARD_WIDTH + 2 * border_size),
                round(CARD_HEIGHT + 2 * border_size),
            ),
            border_size,
        )

    def render(self) -> None:
        if self.is_covered:
            self.draw_covered()
            return

        self.draw_cover()
        self.draw_text()

    @staticmethod
    def check_basic_hit(pos: tuple[int, int], card):
        return (
            card.x <= pos[0] <= card.x + CARD_WIDTH
            and card.y <= pos[1] <= card.y + CARD_HEIGHT
        )

    def check_hit(self, pos: tuple[int, int]) -> bool:
        if not self.check_basic_hit(pos, self):
            return False

        for i in reversed(self.stack):
            if self.check_basic_hit(pos, i):
                return i is self

        return True

    def mouse_down_event(self, mouse_pos: tuple[int, int]) -> None:
        if self.is_covered and not self.is_static:
            return

        if self.is_static:
            self.click_pos = mouse_pos
            self.click_start_static = self.check_hit(mouse_pos)
            return

        if not self.check_hit(mouse_pos):
            return

        if self.dragged:
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
        if self.is_static:
            if not self.click_start_static:
                return self.uncovered_draw_stack, self.total_draw_stack

            if self.check_hit(mouse_pos):
                if len(self.total_draw_stack) == 0:
                    self.total_draw_stack = self.uncovered_draw_stack
                    for i in self.total_draw_stack:
                        i.moveTo(
                            round(STACKS * HORIZONTAL_SPACING + 2 * CORNER_PADDING),
                            CORNER_PADDING,
                        )
                    self.uncovered_draw_stack = []
                    self.click_start_static = False
                    return self.uncovered_draw_stack, self.total_draw_stack

                self.uncovered_draw_stack.append(self.total_draw_stack[0])
                self.uncovered_draw_stack[-1].moveTo(
                    round(STACKS * HORIZONTAL_SPACING + 2 * CORNER_PADDING),
                    CORNER_PADDING,
                )
                self.uncovered_draw_stack[
                    -1
                ].uncovered_draw_stack = self.uncovered_draw_stack
                self.total_draw_stack.pop(0)
                self.click_start_static = False
            return self.uncovered_draw_stack, self.total_draw_stack

        if self.dragged:
            if self.drag_lead:
                center_x = self.x + round(CARD_WIDTH / 2)
                center_y = self.y + round(CARD_HEIGHT / 2)
                closest_stack_index = round(
                    (center_x - CORNER_PADDING - CARD_WIDTH / 2) / HORIZONTAL_SPACING
                )

                if closest_stack_index + 1 > STACKS:
                    closest_stack_index = STACKS - 1

                if closest_stack_index < 0:
                    closest_stack_index = 0

                if len(self.all_stacks[closest_stack_index]) == 0:
                    if not self._value is Value.KING:
                        self.x, self.y = self.drag_start
                        self.drag_lead = False
                        self.dragged = False
                        return self.uncovered_draw_stack

                    closest_card_y_center = CORNER_PADDING + round(CARD_HEIGHT / 2)
                    if abs(closest_card_y_center - center_y) - 20 < CARD_HEIGHT:
                        try:
                            self.stack[self.stack.index(self) - 1].is_covered = False

                        except:
                            pass

                        if self.stack:
                            for index, i in enumerate(
                                self.stack[self.stack.index(self) :]
                            ):
                                print(self.stack)
                                print(self.stack[self.stack.index(self) :])
                                i.x = (
                                    closest_stack_index * HORIZONTAL_SPACING
                                    + CORNER_PADDING
                                )
                                i.y = CORNER_PADDING + VERTICAL_SPACING * index
                                i.dragged = False
                                i.drag_lead = False
                                # new_stack.append(i)
                                self.all_stacks[closest_stack_index].append(i)
                                i.stack.remove(i)
                                i.stack = self.all_stacks[closest_stack_index]
                                return

                        self.x = (
                            closest_stack_index * HORIZONTAL_SPACING + CORNER_PADDING
                        )
                        self.y = CORNER_PADDING
                        print(CORNER_PADDING, self.y)
                        self.dragged = False
                        self.drag_lead = False
                        # new_stack = [
                        #     self,
                        # ]
                        self.all_stacks[closest_stack_index].append(self)
                        self.stack = self.all_stacks[closest_stack_index]
                        self.uncovered_draw_stack.pop(-1)
                        return self.uncovered_draw_stack

                if (
                    closest_stack_index < 0
                    or closest_stack_index > len(self.all_stacks) - 1
                ):
                    return self.uncovered_draw_stack

                closest_card = self.all_stacks[closest_stack_index][-1]
                closest_card_y_center = closest_card.y + round(CARD_HEIGHT / 2)
                if abs(closest_card_y_center - center_y) - 20 < CARD_HEIGHT:
                    if (
                        self._value.value + 1 == closest_card._value.value
                        and self._suit.value % 2 != closest_card._suit.value % 2
                    ):
                        try:
                            self.stack[self.stack.index(self) - 1].is_covered = False

                        except:
                            pass

                        if self.stack:
                            for index, i in enumerate(
                                self.stack[self.stack.index(self) :]
                            ):
                                i.x = closest_card.x
                                i.y = closest_card.y + VERTICAL_SPACING * (index + 1)
                                i.dragged = False
                                i.drag_lead = False
                                closest_card.stack.append(i)
                                i.stack.remove(i)
                                i.stack = closest_card.stack
                            return self.uncovered_draw_stack

                        self.x = closest_card.x
                        self.y = closest_card.y + VERTICAL_SPACING
                        self.dragged = False
                        self.drag_lead = False
                        closest_card.stack.append(self)
                        self.stack = closest_card.stack
                        self.uncovered_draw_stack.pop(-1)
                        return self.uncovered_draw_stack

            self.x, self.y = self.drag_start
            self.drag_lead = False
            self.dragged = False
            return self.uncovered_draw_stack

    def apply_movement(self, mouse_pos: tuple[int, int] = (0, 0)) -> None:
        if self.dragged:
            if not pygame.mouse.get_focused():
                self.dragged = False
                self.drag_lead = False
                self.x, self.y = self.drag_start
                return

            self.x += mouse_pos[0] - self.last_drag_pos[0]
            self.y += mouse_pos[1] - self.last_drag_pos[1]
            self.last_drag_pos = mouse_pos
            # stack_index * 150 + 50

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
    pygame_icon = pygame.image.load("icon.png")
    pygame.display.set_icon(pygame_icon)
    surface = pygame.display.set_mode(WINDOW_SIZE)
    background = pygame.Surface(WINDOW_SIZE)
    background.fill(pygame.Color(BACKGROUND_COLOR))
    return surface, background


is_running = True
surface, background = start()

deck = GameDeck(surface)
draw_x = round(STACKS * HORIZONTAL_SPACING + 2 * CORNER_PADDING)
draw_y = CORNER_PADDING
stacks, draw_stack = get_stacks(deck, True)
draw_stack_current = draw_stack
draw_stack_uncovered = []

draw_card = GameCard(0, 0, surface, True, draw_stack_current, draw_stack_uncovered)
draw_card.moveTo(
    round((STACKS + 1) * HORIZONTAL_SPACING + 2 * CORNER_PADDING), CORNER_PADDING
)
draw_card.is_covered = True


def draw_empty_stack(surface: pygame.Surface):
    for ix in range(2):
        color = (108, 167, 88)
        border_size = ceil(2 * RENDER_FACTOR)
        border_color = (43, 67, 35)
        radius = round(30 * RENDER_FACTOR)
        circle_border = round(5 * RENDER_FACTOR)

        pygame.draw.rect(
            surface,
            color,
            pygame.Rect(
                draw_x + ix * (HORIZONTAL_SPACING),
                draw_y,
                CARD_WIDTH,
                CARD_HEIGHT,
            ),
        )
        pygame.draw.rect(
            surface,
            border_color,
            pygame.Rect(
                draw_x + ix * (HORIZONTAL_SPACING) - border_size,
                draw_y - border_size,
                round(CARD_WIDTH + 2 * border_size),
                round(CARD_HEIGHT + 2 * border_size),
            ),
            border_size,
        )

        pygame.draw.circle(
            surface,
            border_color,
            (
                draw_x + ix * (HORIZONTAL_SPACING) + CARD_WIDTH / 2,
                draw_y + CARD_HEIGHT / 2,
            ),
            radius,
            width=circle_border,
        )


for stack_index, stack in enumerate(stacks):
    for card_index, card in enumerate(stack):
        card.moveTo(
            stack_index * HORIZONTAL_SPACING + CORNER_PADDING,
            card_index * VERTICAL_SPACING + CORNER_PADDING,
        )
        if not card_index == len(stack) - 1:
            card.is_covered = True

for i in draw_stack_current:
    i.all_stacks = stacks

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            draw_card.mouse_down_event(pygame.mouse.get_pos())
            if len(draw_stack_uncovered) > 0:
                # draw_stack_uncovered[-1].uncovered_draw_stack = draw_stack_uncovered
                draw_stack_uncovered[-1].mouse_down_event(pygame.mouse.get_pos())

            for stack in stacks:
                for card in stack:
                    card.mouse_down_event(pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            draw_stack_uncovered, draw_stack_current = draw_card.mouse_up_event(
                pygame.mouse.get_pos()
            )

            if len(draw_stack_uncovered) > 0:
                # draw_stack_uncovered[-1].uncovered_draw_stack = draw_stack_uncovered
                draw_stack_uncovered[-1].mouse_up_event(pygame.mouse.get_pos())

            for stack in stacks:
                for card in stack:
                    card.mouse_up_event(pygame.mouse.get_pos())

    surface.blit(background, (0, 0))
    late_render = []
    draw_empty_stack(surface)
    if len(draw_stack_current) > 0:
        draw_card.render()

    for i in draw_stack_uncovered[:-1]:
        i.render()

    for stack in stacks:
        for card in stack:
            if card.dragged:
                late_render.append(card)
                continue
            card.mainloop(mouse_pos=pygame.mouse.get_pos())

    if len(draw_stack_uncovered) > 0:
        draw_stack_uncovered[-1].mainloop(pygame.mouse.get_pos())

    for card in late_render:
        card.mainloop(mouse_pos=pygame.mouse.get_pos())

    pygame.display.update()
