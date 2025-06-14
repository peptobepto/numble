from logic import NumbleGame

# Generate a random 5-digit number
import random
solution = f"{random.randint(0, 99999):05}"

# Print it so you know the correct answer (for now)
print("SOLUTION:", solution)

# Create the game
game = NumbleGame(solution)

# Let the user type in a guess from terminal for now
guess = input("Enter your 5-digit guess: ")
feedback = game.submit_guess(guess)
print("FEEDBACK:", feedback)
