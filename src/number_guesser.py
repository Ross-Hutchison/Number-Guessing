import re
import random

play = False
internal_difficulty = "unassigned"  # used by the code to carry out checks
external_difficulty = "unassigned"  # output to the user
max_value = -1  # the maximum value the number can be - currently unnasigned
number_of_guesses = -1  # the maximum number of guesses the user has - currently unnasigned
guesses_left = -1   # the number of guesses remaining
answer = -1     # the value the user must guess
score = -1      # the number of correct guesses in a row
file = open("high_scores.txt", "r+t")   # the high score file
file_content = []   # array for storing high score content for editing
high_score = "unassigned"   # the value of the high score to be writen to the file
high_score_name = "unassigned"  # the name of the high scorer to be writen to the file


# asks if the user would like to play altering the value of the relevant boolean
def start():
    global play
    global score
    global file

    print("\n-------------\n")
    ans = input("would you like to play? (y/n)\n")
    while not bool(re.search("^[yn]$", ans)):
        ans = input("would you like to play? (y/n)\n")
    if ans == "n":
        print("fair enough then\n")
        exit(0)
    else:
        play = True
        score = 0


def select_difficulty():
    global internal_difficulty
    global max_value
    global number_of_guesses
    global file_content

    print("select difficulty\n")
    while not bool(re.search("^[1234]$", internal_difficulty)):
        internal_difficulty = input("easy - 1   medium - 2   hard - 3   masochist - 4\n")

    if internal_difficulty == "1":
        max_value = 5
        number_of_guesses = 3
    elif internal_difficulty == "2":
        max_value = 10
        number_of_guesses = 4
    elif internal_difficulty == "3":
        max_value = 15
        number_of_guesses = 4
    elif internal_difficulty == "4":
        max_value = 20
        number_of_guesses = 3

    if max_value == -1:
        print("an error has occurred max value not initialised\n")
        exit(1)
    elif number_of_guesses == -1:
        print("an error has occurred number of guesses not initialised\n")
        exit(1)

    file_content = read_from_hs_file()

    print("enter stop in place of an answer to exit early\n")


def start_round():
    global answer
    global max_value
    global number_of_guesses
    global guesses_left
    global external_difficulty
    global high_score_name
    global high_score
    global score

    answer = random.randrange(1, max_value)

    if answer == -1:
        print("an error has occurred answer not initialised\n")
        exit(1)

    guesses_left = number_of_guesses
    correct = False
    read_from_hs_array()

    print(external_difficulty + " high score is: " + str(high_score) + " held by: " + high_score_name + '\n')
    print("guess a whole number between 1 and " + str(max_value) + " inclusive\n")

    while (not correct) and (guesses_left != 0):
        print(str(guesses_left) + " guesses left\n")

        attempt = input()

        while not bool(re.search("^\d+$|^stop$", attempt)):
            attempt = input("invalid input enter a number or stop\n")
        while (not bool(re.search("^stop$", attempt))) and (int(attempt) > max_value):
            attempt = input("input too high max is " + str(max_value) + '\n')

        if bool(re.search("^stop$", attempt)):
            return False

        if int(attempt) == answer:
            correct = True
        else:
            guesses_left -= 1
            if int(attempt) > answer:
                print("incorrect: value was too high\n")
            else:
                print("incorrect: value was too low\n")

    if correct:
        print("correct!\n")
        score += 1
        return True
    elif guesses_left == 0:
        print("out of tries : (\n")
        return False


def output_score():
    global score
    global internal_difficulty
    global external_difficulty
    global file_content
    global high_score
    global high_score_name

    print("your score was: " + str(score) + '\n')

    if score > int(high_score):
        print("New high score!\n")
        new_name = input("enter your name\n")
        while len(new_name.strip()) > 10:
            new_name = input("invalid: please use a name of no more than 10 characters\n "
                             "spaces at start and end will be removed\n")

        new_data = external_difficulty + "," + new_name.strip() + "," + str(score)
        file_content[int(internal_difficulty) - 1] = new_data

        score = 0


def check_for_replay():
    global play

    ans = input("would you like to play again? (y/n)\n")
    while not bool(re.search("^[yn]$", ans)):
        ans = input("would you like to play? (y/n)\n")

    if ans == "y":
        play = True
    else:
        play = False


def stop():
    update_hs_file()
    print("thank you for playing : )\n")
    print("\n-------------\n")
    file.close()


def update_hs_file():
    global file
    global file_content

    file.close()
    file = open("high_scores.txt", "w")

    content_str = ""
    for x in file_content:
        content_str = content_str + x + '\n'

    file.write(content_str)


def read_from_hs_file():
    global file

    content = file.read()
    separated = content.split('\n')

    return separated


def read_from_hs_array():
    global file_content
    global internal_difficulty
    global external_difficulty
    global high_score_name
    global high_score

    line = file_content[int(internal_difficulty) - 1]
    parts = line.split(',')

    external_difficulty = parts[0]
    high_score_name = parts[1]
    high_score = int(parts[2])


if __name__ == "__main__":
    start()
    select_difficulty()
    while play:
        passed = start_round()
        if not passed:
            output_score()
            check_for_replay()
    stop()
