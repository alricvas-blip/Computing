import random

def get_temperature(guess, secret):
    """Return temperature based on how close the guess is to the secret number."""
    distance = abs(guess - secret)
    if distance == 0:
        return "correct!"
    elif distance <= 2:
        return "very hot"
    elif distance <= 5:
        return "hot"
    elif distance <= 10:
        return "warm"
    elif distance <= 20:
        return "cool"
    else:
        return "cold"

        def main():
            """Main game loop."""
            secret = random.randint(1, 100)
            
            while True:
                guess = int(input("Guess a number between 1 and 100: "))
                distance = abs(guess - secret)
                
                if distance == 0:
                    print("Correct!")
                    break
                elif distance <= 5:
                    print("Very close!")
                elif distance <= 20:
                    print("Getting warm")
                else:
                    print("Cold")

        if __name__ == "__main__":
            main()

def play_game(high_scores):
    """Play a single game of number guessing."""
    secret = random.randint(1, 100)
    guesses = 0
    
    print("\nGuess a number between 1 and 100!")
    
    while True:
        try:
            guess = int(input("Enter your guess: "))
            
            if guess < 1 or guess > 100:
                print("Please enter a number between 1 and 100.")
                continue
            
            guesses += 1
            temp = get_temperature(guess, secret)
            
            if guess > secret:
                print(f"Too high! {temp}")
            elif guess < secret:
                print(f"Too low! {temp}")
            else:
                print(f"Correct! You got it in {guesses} guess(es)!")
                
                # Update high scores
                if not high_scores:
                    high_scores = {"min": guesses, "max": guesses}
                else:
                    high_scores["min"] = min(high_scores["min"], guesses)
                    high_scores["max"] = max(high_scores["max"], guesses)
                
                print(f"Best game: {high_scores['min']} guesses | Worst game: {high_scores['max']} guesses")
                break
                
        except ValueError:
            print("Please enter a valid number.")

def main():
    """Main game loop."""
    high_scores = None
    
    while True:
        play_game(high_scores)
        if high_scores is None:
            high_scores = {"min": 0, "max": 0}
        
        play_again = input("\nPlay again? (yes/no): ").lower()
        if play_again != "yes" and play_again != "y":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()