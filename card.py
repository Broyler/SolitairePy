from enum import Enum
from random import shuffle


class Suit(Enum):
    DIAMOND = 0
    CLUB = 1
    HEART = 2
    SPADE = 3


class Value(Enum):
    ACE = 0
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
    SIX = 5
    SEVEN = 6
    EIGHT = 7
    NINE = 8
    TEN = 9
    JACK = 10
    QUEEN = 11
    KING = 12


SUITS = len(Suit)
VALUES = len(Value)
STACKS = 7


class Card:
    def __init__(self, suit: Suit, value: Value):
        self._suit = Suit(suit) if type(suit) is int else suit
        self._value = Value(value) if type(value) is int else value

    def __repr__(self) -> str:
        return f"{self._value.name.capitalize()} of {self._suit.name.lower()}s"

    def true_value(self) -> str:
        if self._value.value < Value.JACK.value and not self._value is Value.ACE:
            return str(self._value.value + 1)
        return str(self._value.name)[0]

    def card_color(self) -> tuple[int, int, int]:
        if self._suit in [Suit.DIAMOND, Suit.HEART]:
            return (255, 0, 0)
        return (0, 0, 0)

    def suit_symbol(self) -> str:
        return ["♦", "♣", "♥", "♠"][self._suit.value]


class Deck:
    def __init__(self, cards: list[Card] = None):
        if cards:
            self._deck = cards
            return
        self._deck = []
        self.fill()

    @property
    def deck(self):
        return self._deck

    def fill(self) -> None:
        for suit in range(SUITS):
            for values in range(VALUES):
                self._deck.append(Card(suit, values))
        shuffle(self._deck)


def get_stacks(deck: Deck, append_stack: bool = False) -> list[Deck]:
    total = 0
    stacks = []
    for i in range(STACKS):
        stacks.append(deck.deck[total : total + i + 1])
        total += i + 1

    if append_stack:
        for stack in stacks:
            for card in stack:
                card.stack = stack
                card.all_stacks = stacks
    return stacks, deck.deck[total:]


deck = Deck()
stacks = get_stacks(deck)
