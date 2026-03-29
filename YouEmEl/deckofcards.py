import random
from enum import Enum, auto

class Suit(Enum):
    HEARTS = "Hearts"
    DIAMONDS = "Diamonds"
    CLUBS = "Clubs"
    SPADES = "Spades"

class Rank(Enum):
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "Jack"
    QUEEN = "Queen"
    KING = "King"
    ACE = "Ace"

class Card:
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self) -> str:
        return f"{self.rank.value} of {self.suit.value}"

class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in Suit for rank in Rank]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self) -> Card:
        if not self.cards:
            raise ValueError("No cards left in the deck")
        return self.cards.pop()

    def __len__(self) -> int:
        return len(self.cards)

if __name__ == "__main__":
    deck = Deck()
    print(f"Created a deck with {len(deck)} cards.")
    deck.shuffle()
    print("Shuffled the deck.")
    card = deck.deal()
    print(f"Dealt: {card}")
    print(f"Cards remaining: {len(deck)}")
