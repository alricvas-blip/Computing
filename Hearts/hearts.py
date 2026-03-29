import random

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def __repr__(self):
        return self.__str__()

class Deck:
    def __init__(self):
        self.cards = []
        # Reordered ranks to standard order: 2-10, Jack, Queen, King, Ace
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        for s in suits:
            for r in ranks:
                self.cards.append(Card(r, s))

    def shuffle(self):
        random.shuffle(self.cards)

    def show(self):
        for card in self.cards:
            print(card)

if __name__ == "__main__":
    my_deck = Deck()
    my_deck.shuffle()
    my_deck.show()
