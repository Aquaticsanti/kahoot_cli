from kahoot_cli import *
if __name__ == "__main__":
    def printSelectedAnswer(options: list, option_no: int = 0, question_type: str = "Quiz", picked_options: list = []):
        if question_type == "Quiz":
            if option_no == 0:
                print(colored(f"> {options[0]}", "red", None, ["bold"]))
                print(colored(f"  {options[1]}", "blue", None, ["bold"]))
                if len(options) >= 3:
                    print(colored(f"  {options[2]}", "yellow", None, ["bold"]))
                if len(options) >= 4:
                    print(colored(f"  {options[3]}", "green", None, ["bold"]))
            elif option_no == 1:
                print(colored(f"  {options[0]}", "red", None, ["bold"]))
                print(colored(f"> {options[1]}", "blue", None, ["bold"]))
                if len(options) >= 3:
                    print(colored(f"  {options[2]}", "yellow", None, ["bold"]))
                if len(options) >= 4:
                    print(colored(f"  {options[3]}", "green", None, ["bold"])) 
            if option_no == 2:
                print(colored(f"  {options[0]}", "red", None, ["bold"]))
                print(colored(f"  {options[1]}", "blue", None, ["bold"]))
                if len(options) >= 3:
                    print(colored(f"> {options[2]}", "yellow", None, ["bold"]))
                if len(options) >= 4:
                    print(colored(f"  {options[3]}", "green", None, ["bold"]))
            elif option_no == 3:
                print(colored(f"  {options[0]}", "red", None, ["bold"]))
                print(colored(f"  {options[1]}", "blue", None, ["bold"]))
                if len(options) >= 3:
                    print(colored(f"  {options[2]}", "yellow", None, ["bold"]))
                if len(options) >= 4:
                    print(colored(f"> {options[3]}", "green", None, ["bold"]))
        elif question_type == "TorF":
            if option_no == 0:
                print(colored(f"> {options[0]}", "blue", None, ["bold"])) # Yes, red is blue and blue is red. I know that.
                print(colored(f"  {options[1]}", "red", None, ["bold"]))
            elif option_no == 1:
                print(colored(f"  {options[0]}", "blue", None, ["bold"]))
                print(colored(f"> {options[1]}", "red", None, ["bold"]))
        elif question_type == "Multi":
            if option_no == 0:
                print(colored(f"> {options[0]}", "red", None, ["bold"]))
            elif option_no != 0:
                if 0 in picked_options:
                    print(colored(">", "white", None, ["bold"]) ,colored(f"{options[0]}", "red", None, ["bold"]))
                else:
                    print(colored(f"  {options[0]}", "red", None, ["bold"]))
            if option_no == 1:
                print(colored(f"> {options[1]}", "blue", None, ["bold"]))
            elif option_no != 1:
                if 1 in picked_options:
                    print(colored(">", "white", None, ["bold"]), colored(f"{options[1]}", "blue", None, ["bold"]))
                else:
                    print(colored(f"  {options[1]}", "blue", None, ["bold"]))
            if option_no == 2 and len(options) >= 3:
                print(colored(f"> {options[2]}", "yellow", None, ["bold"]))
            elif option_no != 2 and len(options) >= 3:
                if 2 in picked_options:
                    print(colored(">", "white", None, ["bold"]), colored(f"{options[2]}", "yellow", None, ["bold"]))
                else:
                    print(colored(f"  {options[2]}", "yellow", None, ["bold"]))
            if option_no == 3 and len(options) >= 4:
                print(colored(f"> {options[3]}", "green", None, ["bold"]))
            elif option_no != 3 and len(options) >= 4:
                if 3 in picked_options:
                    print(colored(">", "white", None, ["bold"]), colored(f"{options[3]}", "green", None, ["bold"]))
                else:
                    print(colored(f"  {options[3]}", "green", None, ["bold"])) 
            if option_no == amountOptions:
                if picked_options == []:
                    print(colored(f"> SUBMIT", "dark_grey", None, ["bold"]))
                else:
                    print(colored(f"> SUBMIT", "white", None, ["bold"]))
            elif option_no != amountOptions:
                if picked_options == []:
                    print(colored(f"  SUBMIT", "dark_grey", None, ["bold"]))
                else:
                    print(colored(f"  SUBMIT", "white", None, ["bold"]))
    correctMessages = ["Way to go, superstar!", "Amazing!", "Trust me, your oponents are jealous.", "One step closer to victory!", "Keep the flame lit!"]
    wrongMessages = ["Don't worry, you'll get them next time!", "Never back down never what?", "Nice try!"]


    print(colored("""
██╗░░██╗░█████╗░██╗░░██╗░█████╗░░█████╗░████████╗░░░░░░░█████╗░██╗░░░░░██╗
██║░██╔╝██╔══██╗██║░░██║██╔══██╗██╔══██╗╚══██╔══╝░░░░░░██╔══██╗██║░░░░░██║
█████═╝░███████║███████║██║░░██║██║░░██║░░░██║░░░█████╗██║░░╚═╝██║░░░░░██║
██╔═██╗░██╔══██║██╔══██║██║░░██║██║░░██║░░░██║░░░╚════╝██║░░██╗██║░░░░░██║
██║░╚██╗██║░░██║██║░░██║╚█████╔╝╚█████╔╝░░░██║░░░░░░░░░╚█████╔╝███████╗██║
╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░░╚════╝░░░░╚═╝░░░░░░░░░░╚════╝░╚══════╝╚═╝""", (100, 53, 173)))

    print("Welcome to Kahoot_CLI! Made by @Aquaticsanti\n")

    client = KahootClient()
    pin = ""

    while True:
        try:
            if pin == "":
                pin = input("Input the game pin: ")
                if "https://kahoot.it" in pin: # For development purposes, this also takes copied links (I do not want to copy the pin manually)
                    pass
                else:
                    pin = pin.replace(" ", "")
                    pin = int(pin)
        except ValueError:
                pin = input("That doesn't look like a number... Please input the game pin: ")
                if "https://kahoot.it" in pin: # For development purposes, this also takes copied links (I do not want to copy the pin manually)
                    pass
                else:
                    pin = int(pin)
        else:
            break

    while True:
        try:
            joinedGame = client.JoinGame(pin)
        except InvalidPinError:
            try:
                pin = input("Uh oh, the pin is invalid. Input the game pin (no spaces): ")
                if "https://kahoot.it/" in pin:
                    pass
                else:
                    pin = int(pin)
            except ValueError:
                pin = input("That doesn't look like a number... Please input the game pin (no spaces): ")
                if "https://kahoot.it/" in pin:
                    pass
                else:
                    pin = int(pin)
            joinedGame = client.JoinGame(pin)
        else:
            break

    if joinedGame == "ok":
        validNickname = False
        nickname = input("What's your name? (Don't use your real name): ")
        while validNickname != True:
            if nickname == "":
                nickname = input("Uh oh, looks like your nickname is blank. Please choose a valid nickname (Don't use your real name): ")
            elif len(nickname) > 15:
                nickname = input("Uh oh, looks like your nickname is too long. Please choose a nickname with less than 15 characters (Don't use your real name): ")
            else:
                try:
                    nicknameSet = client.SetNickname(nickname)
                except InvalidNameError:
                    nickname = input("Uh oh, looks like your nickname was taken. Please choose another nickname (Don't use your real name): ")
                else:
                    break
        
    elif joinedGame == "namerator":
        print("This game uses a random name generator!")
        print("Press", colored("enter", None, None, ["italic"]), "to re-roll, and", colored("space", None, None, ["italic"]), "to select!")
        spins = 3
        while True:
            keypress = readkey()
            if keypress == key.ENTER:
                if spins > 0:
                    spins -= 1
                    print("Rolling...", end="\r")
                    nickname = client.Namerator(roll = True)
                    print("Your nickname is...", colored(nickname, None, None, ["bold"]))
                    print(colored(f"{spins} spins left", "dark_grey"))
                else:
                    print("Uh oh, looks like there's no spins left! Please press", colored("space", None, None, ["italic"]), "to select.")
            elif keypress == key.SPACE:
                try:
                    nickname = client.Namerator(keep=True)
                except NameratorError:
                    print("Please roll once!")
                else:
                    break
            

    while True:
        CurrentState = client.ClientState()
        if CurrentState == "Lobby":
            try:
                if nicknameSet != "": # Check if random name generator wasn't used
                    pass
            except NameError:
                print("You're in! See your name on the screen?")
            else:
                if nicknameSet not in ["ok", "twoauth"]:
                    nickname = nicknameSet
                    print(f"Your name has been changed to {nickname}")
                else:
                    print("You're in! See your name on the screen?")
            print(colored("Note: Reactions and avatars are not supported yet.", "dark_grey"))
            break
        elif CurrentState == "Quiz":
            break
        elif CurrentState == "TwoAuth":
            try:
                if AuthValid == True:
                    pass # This is supposed to check if the combo exists, AKA if it's the first time inputting the code
            except NameError:
                print("Looks like this game uses 2FA! Please input the combination shown on screen.")
                print(colored("r", "red"), "for", colored("red", "red"), end=", ")
                print(colored("b", "blue"), "for", colored("blue", "blue"), end=", ")
                print(colored("y", "yellow"), "for", colored("yellow", "yellow"), end=", ")
                print("and", colored("g", "green"), "for", colored("green", "green"))
            else:
                print("Please input the combination shown on screen.")
            combo = input()
            while True:
                if len(combo) != 4:
                    combo = input("That combo is invalid, please try again: ")
                else:
                    combo2 = []
                    for char in combo:
                        if char not in ["r", "b", "y", "g", "R", "B", "Y", "G"]:
                            combo = input("That combo is invalid, please try again: ")
                            break
                        else:
                            combo2.append(char.lower())
                    if len(combo) == 4: # Not the best solution, but I guess it works?
                        break
            AuthValid = client.TwoAuth(combo2)
            time.sleep(0.5)
            if AuthValid == False:
                print("Uh oh, that combo was invalid.")
            else:
                pass
        if CurrentState == "Out":
            print("Uh oh, looks like you've been kicked out. Exiting...")
            os._exit(1) # Source - https://stackoverflow.com/a/49950466
        if CurrentState == "Quiz" or CurrentState == "Start":
            break
    
    while True:
        CurrentState = client.ClientState()
        if CurrentState == "Start":
            print("Get ready!")
            question_no = 1
            break
        elif CurrentState == "Quiz":
            break


    while True: # This encapsulates the whole game logic.
        CurrentState = client.ClientState()
        while CurrentState != "Quiz":
            CurrentState = client.ClientState()

        cls() # Source - https://stackoverflow.com/a/684344, Clears entire CLI

        question = client.GetQuestion()
        total_points = client.GetPoints()
        optionList = question[3:]
        print(colored(f"{client.nickname} - {total_points} points", "dark_grey"))
        if question[0] == "Quiz" or question[0] == "TorF":
            if question[1] != "":
                print(f"Question {question[2]} - {question[1]}")
            else:
                print(f"Question {question[2]}")
        elif question[0] == "Multi":
            if question[1] == "":
                print(f"Question {question[2]}", colored(" (MULTIPLE CHOICE!)", None, None, ["bold"]))
            else:
                print(f"Question {question[2]} - {question[1]}", colored(" (MULTIPLE CHOICE!)", None, None, ["bold"]))

        amountOptions = len(question) - 3
        
        if question[0] == "Multi":
            amountOptions += 1 # To account for the submit button
            picked_ans = []

        selected_ans = 0

        printSelectedAnswer(optionList, selected_ans, question[0])
        while True:
            CurrentState = client.ClientState(fast=True)
            if CurrentState == "Res":
                break
            keypress = readkey()
            if keypress == key.RIGHT or keypress == key.LEFT:
                continue
            print(f"\033[{amountOptions+1}A") # Moves cursor up x lines, Source - https://stackoverflow.com/a/72667369
            if keypress == key.UP:
                CurrentState = client.ClientState(fast=True)
                if CurrentState == "Res":
                    break
                selected_ans -= 1
                if selected_ans < 0:
                    selected_ans = amountOptions
                if question[0] != "Multi":
                    printSelectedAnswer(optionList, selected_ans, question[0])
                else:
                    printSelectedAnswer(optionList, selected_ans, question[0], picked_ans)
            if keypress == key.DOWN:
                CurrentState = client.ClientState(fast=True)
                if CurrentState == "Res":
                    break
                selected_ans += 1
                if selected_ans > amountOptions:
                    selected_ans = 0
                if question[0] != "Multi":
                    printSelectedAnswer(optionList, selected_ans, question[0])
                else:
                    printSelectedAnswer(optionList, selected_ans, question[0], picked_ans)
            if keypress == key.ENTER:
                CurrentState = client.ClientState(fast=True)
                if CurrentState == "Res":
                    break
                if question[0] == "Quiz" or question[0] == "TorF":
                    printSelectedAnswer(optionList, selected_ans, question[0])
                    client.AnswerQuestion(selected_ans)
                    break
                elif question[0] == "Multi":
                    printSelectedAnswer(optionList, selected_ans, question[0], picked_ans)
                    if selected_ans == 0:
                        if 0 not in picked_ans:
                            picked_ans.append(0)
                        elif 0 in picked_ans:
                            picked_ans.remove(0)
                    elif selected_ans == 1:
                        if 1 not in picked_ans:
                            picked_ans.append(1)
                        elif 1 in picked_ans:
                            picked_ans.remove(1)
                    elif selected_ans == 2:
                        if 2 not in picked_ans:
                            picked_ans.append(2)
                        elif 2 in picked_ans:
                            picked_ans.remove(2)
                    elif selected_ans == 3:
                        if 3 not in picked_ans:
                            picked_ans.append(3)
                        elif 3 in picked_ans:
                            picked_ans.remove(3)
                    elif selected_ans == amountOptions:
                        if picked_ans == []:
                            continue
                        else:
                            client.AnswerQuestion(picked_ans)
                            break           

        while CurrentState != "Res":
            CurrentState = client.ClientState(True)
        result = client.GetResult()
        if type(result) == str:
            if result == "NoTime":
                print(colored("You ran out of time...", "red", None, ["bold"]))
                print(wrongMessages[random.randrange(len(wrongMessages))])
            elif result == "Lose":
                print(colored("Wrong...", "red", None, ["bold"]))
                print(wrongMessages[random.randrange(len(wrongMessages))])
        else:
            if result[0] == "Win":
                print(colored(f"Correct! {result[1]} points", "green", None, ["bold"]))
                print(correctMessages[random.randrange(len(correctMessages))])
            else:
                print(colored("Partially Correct", "light_blue", None, ["bold"]), f"- {result[0]} right answers, for {result[1]} points")

        leaderboard_pos = client.GetLeaderboardPos()
        leaderboard_pos_int = str(leaderboard_pos[0])
        leaderboard_pos_int += "th"
        if leaderboard_pos[0] != "Podium":
            print(f"You're in {leaderboard_pos_int} place,", leaderboard_pos[1])
        else:
            print("You're in the podium!")

        while True: # Check if game has finished, or if there's another question
            CurrentState = client.ClientState(fast=True)
            if CurrentState == "Quiz":
                finished = False
                break
            elif CurrentState == "End":
                finished = True
                cls()
                break
            else:
                pass

        if finished == False:
            pass
        elif finished == True:
            break

    ranking = client.GetFinalRanking()

    if ranking not in [0, 1, 2, 3]:
        ranking = str(ranking)
        leaderboard_pos_int += "th"
        while True:
            try:
                total_points = client.GetPoints()
            except:
                pass
            else:
                break
        print(f"You got {ranking} place, with a total of {total_points} points!!")
    else:
        print("Drumroll please...")
        while True:
            # TODO: Checkea q todo funcione, aca estaba fallando.
            ranking = client.GetFinalRanking()
            if ranking == 3:
                total_points = client.GetPoints()
                podiumPlace = 3
                print("You got", colored("3rd place,", (205, 127, 50)), f"with a total of {total_points} points!")
                break
            elif ranking == 2:
                total_points = client.GetPoints()
                print("You got", colored("2nd place,", (192, 192, 192)), f"with a total of {total_points} points!")
                break
            elif ranking == 1:
                total_points = client.GetPoints()
                print("You got", colored("1st place,", (255, 215, 0)), f"with a total of {total_points} points!")
                break
            else:
                pass

