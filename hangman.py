# Author - Srikkanth Govindaraajan

# Python Imports
import logging
import random
import re
import requests
import time
import os

high_score_file = "high_score.txt"
fh = open(high_score_file,'w+')
if os.stat(high_score_file).st_size == 0:
    print "**** Good Luck to set an high score ****"
else:
    print "Least time to find the word is " + fh.read() + " seconds"
fh.close()

# Function to display HANGMAN message
def check_hangman(fail_count):
    """ 
    Function to display HANGMAN message
    for a particular fail count number. 
    
    Returns 'None'
        - parameters using ``:param fail_count : Number of wrong guesses by the user``
        - type of parameters ``:type integer : integer >0 and less than 8
        - examples:
        check_hangman(5)
        Output -  You have 'HANGM' now
    """
    if(fail_count == 1):
        print "You have 'H' now"
    elif(fail_count == 2):
        print "You have 'HA' now"
    elif(fail_count == 3):
        print "You have 'HAN' now"
    elif(fail_count == 4):
        print "You have 'HANG' now"
    elif(fail_count == 5):
        print "You have 'HANGM' now"
    elif(fail_count == 6):
        print "You have 'HANGMA' now"
    else:
        print "You are HANGED!"
    return

def draw_dashes_or_alphabet(of_type,word_length=None,index=None):
    """
        Function to draw the hangman console with dashes and 
        fill the appropriate position when a corresponding 
        alphabet is found. 
    """
    global word_print
    global success
    if of_type == "dashes":
        success = 0
        word_print = ["_"] * word_length
    else:
        success +=1
        word_print[index] = c
        if success == word_length:
            print "Congrats you found the word ---> " + correct_word
            end_time = time.time()
            print "You found the word in " + str(int(end_time - start_time)) + " seconds"
            
            if os.stat(high_score_file).st_size != 0:
                # If file size is not zero, then some score already exists in the file.
                fh = open(high_score_file,'r')
                previous_score = fh.read()
                fh.close()
            
                # Time taken to guess word is less than what is in file, then overwrite.
                if int(previous_score) > (end_time - start_time):
                    fh = open(high_score_file,'w')
                    fh.write(str(int(end_time - start_time)))    
                    fh.close()
            else:
                # No new scores yet
                fh = open(high_score_file,'w')
                fh.write(str(int(end_time - start_time)))
                fh.close()   
            exit(0)
    
    if success != 0:
        print "\n\n \tWord Guessed Till now:\n"
    
    print " ".join(word_print[0:word_length])
    print "\n\n"

# Get a dictionary from remote location and parse it to choose random words for the game
words_site_remote = "https://raw.githubusercontent.com/dwyl/english-words/master/words2.txt"
response = requests.get(words_site_remote)
words = response.content.splitlines()

# Log the word in a sample log file
logging.basicConfig(filename='example.log',level=logging.DEBUG)
correct_word = random.choice(words)
correct_word = correct_word.lower()
print "This is a " + str(len(correct_word)) + " letter word "

# Draw initial hangman console
draw_dashes_or_alphabet("dashes",word_length=len(correct_word))
logging.info("Word to be guessed is " + correct_word)

# Initialize variables
right_guess = False
fail_count = 0
wrong_guesses = []
correct_guesses = []

start_time = time.time()
while right_guess == False:
    # Get input character
    c = raw_input("Enter a alphabet:")
    
    if not c.isalpha():
        print "This kind of input not allowed. Please enter a letter"
        continue
    
    if c in correct_guesses:
        print "You already guessed letter " + c + "! Keep guessing."
        continue
    
    # Print the wrong Guesses to help the user
    if len(wrong_guesses) > 0:
        print "Wrong guesses so far " + str(wrong_guesses)

    # Check if the character entered is present in the string
    if c in correct_word.lower():
        # User regular expressions to get all index(es) if the character is present more than once
        correct_guesses.append(c)
        iter_match = re.finditer(c,correct_word)
        for match in iter_match:
            print c + " found at position(s) " + str(match.start())
            
            # Fill the hangman console with the character
            draw_dashes_or_alphabet(c,index=match.start(), word_length = len(correct_word))
        
        # Prompt the user to type the word if he/she has guessed more than 50% of the word
        if success == (len(correct_word)/2):
            choice = raw_input("Have you guessed the word? (y/n)")
            if choice == "y":
                word = raw_input("Enter the word: ")
                if word == correct_word.lower():
                    # Guessed the right word
                    print "Congrats you found the word ---> " + correct_word
                    end_time = time.time()
                    print "You found the word in " + str(int(end_time - start_time)) + " seconds"
                    
                    if os.stat(high_score_file).st_size != 0:
                        # If file size is not zero, then some score already exists in the file.
                        fh = open(high_score_file,'r')
                        previous_score = fh.read()
                        fh.close()
                    
                        # Time taken to guess word is less than what is in file, then overwrite.
                        if int(previous_score) > (end_time - start_time):
                            fh = open(high_score_file,'w')
                            fh.write(str(int(end_time - start_time)))    
                            fh.close()
                    else:
                        # No new scores yet
                        fh = open(high_score_file,'w')
                        fh.write(str(int(end_time - start_time)))
                        fh.close()   
                    exit(0)
                else:
                    # Wrong word, so increment hangman fail count
                    print "Oops wrong, increasing fail count"
                    fail_count += 1
                    check_hangman(fail_count)
                    # Check if fail_count is 7 which is number of letters in HANGMAN, if so game over!
                    if fail_count == 7:
                        print "Game over! The word was " + correct_word
                        exit(0)
            else:
                # User enter 'n' for guessed the word prompt - so continue the next iteration of while loop
                continue
    elif c in wrong_guesses:
        print "\n You already guessed alphabet " + c + " and it was not found. Not increasing fail count"
        continue
    else:
        # Character entered not present in word, increase fail count
        fail_count += 1
        
        # Append character entered to the wrong guess list 
        wrong_guesses.append(c)
        
        # CHeck hangman fail count and display message
        check_hangman(fail_count)
        if fail_count == 7:
            print "Game over! The word was " + correct_word
            exit(0)
