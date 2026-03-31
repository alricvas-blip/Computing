import random


secret = random.randint(1, 100)

counter = 0

while True:
    counter += 1
    
    user_number = int(input("Guess the number between 1 and 100: "))

    if user_number == secret:
        print("Congratulations! You guessed the number.")
        print(f"It took you {counter} guesses.")
        break
    elif user_number < secret:
        print("Too low! Try again.")
    else:
        print("Too high! Try again.")

