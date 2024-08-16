import random
print("""                   Hello Everyone we Welcome you in Rock-Paper-Scissors Game
    It's Rule are Simple:
        -> Rock beats Scissors: Rock crushes scissors.
        -> Scissors beat Paper: Scissors cut paper.
        -> Paper beats Rock: Paper covers rock.
      Now let's play the Game.""")
def play_game():
    user_win = 0
    computer_win = 0

    options = ["rock" , "paper" , "scissors"]

    while True :
        user_input = input("Type Rock/Paper/Scissors or Q to Quit ").lower()

        if user_input == "q" :
            print("User win :",user_win,"\nComputer win :",computer_win)
            break

        
        if user_input not in ["rock" , "paper", "scissors"] :
            continue

        random_number = random.randint(0,2)

        # Rock : 0 , Paper : 1 , Scissors : 2'
        computer_guess = options[random_number]
        print("Computer picked",computer_guess+'.')

        if user_input == computer_guess :
                print("It's a tie!")
        elif user_input == 'rock':
            if computer_guess == 'scissors':
                print("You win this round")
                user_win += 1
            else:
                print("Computer wins this round")
                computer_win +=1

        elif user_input == 'paper':
            if computer_guess == 'rock':
                print("You win this round")
                user_win += 1
            else:
                print("Computer wins this round")
                computer_win +=1

        elif user_input == 'scissors' :
            if computer_guess == 'paper':
                print("You win this round")
                user_win += 1
            else:
                print("Computer wins this round")
                computer_win +=1
        else:
            print("Computer wins this round")
            computer_win += 1
        
while True :
    play_game()
    user_choice  = input("Wanna play again : ")
    if user_choice.lower() not in ["yes"or 'y']:
        print("Thank You for playing!")
        break





