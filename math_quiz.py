import random

def choose_theme() :
    print("\nChoose a theme:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("\n")
    print(" ★ ★ ★ Type 'q' anytime during the quiz to quit early  ★ ★ ★ \n")
    
    choice = input("Enter your choice (1-4): ")

    while choice not in ["1", "2", "3", "4" , "q" , "Q"] :
        print ("\nInvalid choice. Please enter a number between 1 and 4.\n")
        choice = input("Enter your choice (1-4): ")
    return choice

def generate_question(theme, difficulty) :
    
    #Easy questions (Year 4 - 8)
    if difficulty == "easy" :
        a = random.randint(1, 30)
        b = random.randint(1, 30)

    #Hard questions (Year 9 - 13)
    else :
        a = random.randint(30, 100)
        b = random.randint(30, 100)

    #Generate questions based on the chosen theme
    if theme == "1" :
        question = f"{a} + {b}"
        answer = a + b

    elif theme == "2" :
        question = f"{a} - {b}"
        answer = a - b  
    
    elif theme == "3" :
        question = f"{a} x {b}"
        answer = a * b

    elif theme == "4" :
       #Ensure division is clean
       answer = random.randint(1, 12)
       b = random.randint(1, 12)
       a = answer * b
       question = f"{a} / {b}"

    return question, answer
    
def play_quiz (theme, difficulty):
    for i in range (30) :
        question, answer = generate_question (theme, difficulty)

        while True :
            user_input = input (f"Question {i+1}/20 : {question} = ")

            if user_input.lower() == 'q' :
                print ("Thanks for playing! Ending quiz early...")
                return
            try : 
                user_input = int(user_input)

                if user_input == answer :
                    print ("\nCorrect!\n")
                    break
                else : 
                    print ("\nWrong answer, try again!\n")
                    
            except :
                print ("\nOops! Please enter a valid number.\n")

def next_action() :

    print ("\nWhat would you like to do next?")
    print ("1. Test your limits (HARD MODE)")
    print ("2. Exit")

    choice = input ("Enter your choice (1 or 2) : ")
    return choice

def main() :
    while True :
        theme = choose_theme()

        if theme == "q" or theme == "Q" :
            action = next_action()

            if action == "1" :
                continue

            elif action == "2" :
                print ("Goodbye!")
                break

        play_quiz (theme, "easy")

        action = next_action()

        if action == "1" :
            play_quiz (theme, "hard")

        elif action == "2" :
            print ("Thanks for playing! Goodbye!")
            break

main()