# Python program to simulate dice.
# Srikkanth Govindaraajan - https://github.com/govindsh

# Steps:
# First, get input number from user - range:1-6
# Roll the dice, random number in the range
# If equal, give another chance
# Else quit the program.

# Import Modules
import random
from sys import argv

# Get the program name
program_name = argv

# Variables
success = 1
score = 0

# Start the while loop
while(success == 1):
    random_number = random.randint(1,6)

    # Get input number from user
    input_number = input("\nEnter number you want range [1-6]:")

    # Compare with random number generated
    if (random_number == input_number):
        # If same, increase score
        score +=1
        print "\nGreat! Dice returned your guess. Continue playing. Score is %d"%score
        continue
    else:
        # Not same, exit the game.
        success = 0
        print "\nSorry! Dice returned %s while you guessed %s"%(random_number,input_number)
# Game over, print score
print "\nDice simulator: GAME OVER!!\nYour score: %d"%score
