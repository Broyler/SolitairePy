from enum import Enum
from random import shuffle


class Suit(Enum):
    CLUB = 0
    DIAMOND = 1
    HEART = 2
    SPADE = 3


class Value(Enum):
    TWO = 0
    THREE = 1
    FOUR = 2
    FIVE = 3
    SIX = 4
    SEVEN = 5
    EIGHT = 6
    NINE = 7
    TEN = 8
    JACK = 9
    QUEEN = 10
    KING = 11
    ACE = 12


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
        if self._value.value < Value.JACK.value:
            return str(self._value.value + 2)
        return str(self._value.name)[0]

    def card_color(self) -> tuple[int, int, int]:
        if self._suit in [Suit.DIAMOND, Suit.HEART]:
            return (255, 0, 0)
        return (0, 0, 0)

    def suit_symbol(self) -> str:
        return ["♣", "♦", "♥", "♠"][self._suit.value]


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


def get_stacks(deck: Deck) -> list[Deck]:
    total = 0
    stacks = []
    for i in range(STACKS):
        stacks.append(deck.deck[total : total + i + 1])
        total += i + 1
    return stacks


deck = Deck()
stacks = get_stacks(deck)
