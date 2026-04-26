import random
from typing import List, Optional

# --- Core Classes (Card, Deck, Pile, Player) ---

class Card:
    """
    Represents a single playing card with a suit and a rank.
    This is a standard class with an __init__ method.
    """
    def __init__(self, suit: str, rank: str):
        self.suit = suit
        self.rank = rank

    def get_value(self) -> int:
        """Calculates the numerical value of a card for comparison. Ace is high."""
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        # We find the index of the rank in the list to get its value.
        value = ranks.index(self.rank) + 2
        return value

    def __repr__(self) -> str:
        """Provides a user-friendly string representation of the card."""
        return f"{self.rank} of {self.suit}"

class Deck:
    """Represents a standard 52-card deck."""
    def __init__(self) -> None:
        self.cards: List[Card] = []
        suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        
        # A standard for-loop to create all 52 cards.
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self) -> None:
        """Shuffles the deck randomly."""
        random.shuffle(self.cards)

    def draw(self) -> Optional[Card]:
        """Draws a single card from the top of the deck."""
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            return None

class Pile:
    """
    Represents the pile of cards in the middle of the table during a trick.
    This class is new for Task 3.
    """
    def __init__(self):
        # This list will hold tuples of (card, player_who_played_it)
        self.cards_in_pile: List = []

    def add_card(self, card: Card, player):
        """Adds a card to the pile, keeping track of who played it."""
        self.cards_in_pile.append((card, player))
        print(f"{player.name} plays {card}")

    def get_lead_card(self) -> Optional[Card]:
        """Returns the first card that was played in the trick."""
        if len(self.cards_in_pile) > 0:
            return self.cards_in_pile[0][0]
        return None

    def clear(self) -> List[Card]:
        """Clears the pile and returns the cards that were in it."""
        # We only need to return the cards, not the players who played them.
        cards = []
        for item in self.cards_in_pile:
            cards.append(item[0])
        
        self.cards_in_pile = []
        return cards

# A helper function to get a sorting key for cards.
# This replaces the lambda function from hearts4.py.
def get_card_sort_key(card: Card):
    """Returns a tuple used for sorting cards by suit, then rank."""
    suit_order = ["Clubs", "Diamonds", "Spades", "Hearts"]
    return (suit_order.index(card.suit), card.get_value())

class Player:
    """Represents a player in the game."""
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.hand: List[Card] = []
        # This new list will store cards won from tricks, as required by Task 3.
        self.captured_cards: List[Card] = []

    def display_hand(self):
        """Displays the player's hand, sorted for readability."""
        print(f"\n{self.name}'s hand:")
        # Sort the hand using the helper function instead of a lambda.
        self.hand.sort(key=get_card_sort_key)
        
        # A standard for-loop to print cards with their index.
        # This replaces the enumerate() function from hearts4.py.
        for i in range(len(self.hand)):
            card = self.hand[i]
            print(f"[{i}] {card}")

    def get_valid_cards(self, lead_suit: Optional[str]) -> List[Card]:
        """
        Determines the list of valid cards a player can play.
        This version is simplified and uses standard for-loops.
        """
        # If the player is leading the trick, they can play any card.
        if not lead_suit:
            return self.hand

        # If following suit, find all cards of the lead suit.
        # This for-loop replaces the list comprehension from hearts4.py.
        follow_suit_cards = []
        for card in self.hand:
            if card.suit == lead_suit:
                follow_suit_cards.append(card)
        
        # If the player has cards of the lead suit, they must play one of them.
        if len(follow_suit_cards) > 0:
            return follow_suit_cards
        
        # If the player cannot follow suit, they can discard any card.
        return self.hand

    def choose_card_to_play(self, lead_suit: Optional[str]) -> Card:
        """
        Allows a player to choose a card to play.
        For simplicity in this non-interactive file, we just play the first valid card.
        """
        valid_cards = self.get_valid_cards(lead_suit)
        # In a real game, you would ask for input here.
        # For this demonstration, we'll just play the last card in the valid list.
        card_to_play = valid_cards[-1]
        self.hand.remove(card_to_play)
        return card_to_play

    def choose_cards_to_pass(self) -> List[Card]:
        """
        Selects 3 cards to pass. For this demo, it passes the 3 highest cards.
        This version uses a standard for-loop instead of a list comprehension.
        """
        print(f"\n{self.name}: Choose 3 cards to pass.")
        self.display_hand()
        # To make this runnable, we'll auto-select the 3 highest cards.
        self.hand.sort(key=get_card_sort_key)
        
        cards_to_pass = []
        # This loop replaces the list comprehension from hearts4.py.
        for _ in range(3):
            # Popping from the end gets the highest cards from the sorted hand.
            cards_to_pass.append(self.hand.pop())
            
        print(f"{self.name} is passing {cards_to_pass[0]}, {cards_to_pass[1]}, {cards_to_pass[2]}")
        return cards_to_pass

class Game:
    """Manages the overall game flow of Hearts for Task 3."""
    def __init__(self, names: List[str]):
        # This for-loop replaces the list comprehension from hearts4.py.
        self.players: List[Player] = []
        for name in names:
            self.players.append(Player(name))
        self.pile = Pile()

    def run_demonstration(self):
        """
        This method runs a single demonstration round showing dealing, passing,
        and playing one trick.
        """
        print("--- Setting up the game ---")
        
        # 1. Deal the cards
        deck = Deck()
        deck.shuffle()
        for _ in range(13):
            for p in self.players:
                card = deck.draw()
                if card:
                    p.hand.append(card)
        
        # Display initial hands
        for p in self.players:
            p.display_hand()
        
        # 2. Passing Phase (Left Only)
        self.passing_phase()
        print("\n--- Hands after passing ---")
        for p in self.players:
            p.display_hand()

        # 3. Play one trick
        self.play_trick()
        
        # 4. Show results
        print("\n--- Results after one trick ---")
        for p in self.players:
            if len(p.captured_cards) > 0:
                print(f"{p.name} captured: {p.captured_cards}")
            else:
                 print(f"{p.name} captured no cards.")

    def passing_phase(self):
        """
        Manages passing 3 cards to the left.
        This is simplified from the hearts4.py version.
        """
        print("\n--- Card Passing Phase (Passing Left) ---")
        
        # This for-loop replaces the list comprehension from hearts4.py.
        all_passed = []
        for p in self.players:
            all_passed.append(p.choose_cards_to_pass())
        
        # Distribute the passed cards. For passing left, player `i` gives
        # their cards to player `(i + 1)`.
        for i in range(len(self.players)):
            receiver_index = (i + 1) % len(self.players)
            cards = all_passed[i]
            self.players[receiver_index].hand.extend(cards)

    def play_trick(self):
        """Manages the logic for a single trick."""
        print("\n--- Playing a Trick ---")
        
        # Find who has the 2 of Clubs to lead the first trick.
        # This loop structure replaces the 'any()' call from hearts4.py.
        leader_idx = 0
        found_leader = False
        for i in range(len(self.players)):
            for card in self.players[i].hand:
                if card.suit == "Clubs" and card.rank == "2":
                    leader_idx = i
                    found_leader = True
                    break
            if found_leader:
                break
        
        print(f"{self.players[leader_idx].name} has the 2 of Clubs and will lead.")

        # The players play in order, starting with the leader.
        for i in range(len(self.players)):
            current_player_index = (leader_idx + i) % len(self.players)
            player = self.players[current_player_index]
            
            lead_card = self.pile.get_lead_card()
            lead_suit = None
            if lead_card:
                lead_suit = lead_card.suit
                
            card_to_play = player.choose_card_to_play(lead_suit)
            self.pile.add_card(card_to_play, player)

        # Determine the winner of the trick.
        lead_card = self.pile.get_lead_card()
        winning_card = lead_card
        winner = self.pile.cards_in_pile[0][1] # The player who led

        for card, player in self.pile.cards_in_pile:
            if card.suit == lead_card.suit:
                if card.get_value() > winning_card.get_value():
                    winning_card = card
                    winner = player
        
        # The winner captures the cards from the pile. This replaces scoring.
        print(f"\n*** {winner.name} wins the trick with the {winning_card}! ***")
        captured = self.pile.clear()
        winner.captured_cards.extend(captured)

# Main execution block.
if __name__ == "__main__":
    game = Game(["Alric", "Bot 1", "Bot 2", "Bot 3"])
    game.run_demonstration()
