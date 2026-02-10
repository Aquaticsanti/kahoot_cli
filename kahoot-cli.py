from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from termcolor import colored
import time
import os
from readchar import readkey, key
import random

def cls(): # Source - https://stackoverflow.com/a/684344
    os.system('cls' if os.name=='nt' else 'clear')

def printSelectedAnswer(option_no: int = 0, question_type: str = "Quiz", picked_options: list = []):
    if question_type == "Quiz":
        if option_no == 0:
            print(colored(f"> {ans_red.text}", "red", None, ["bold"]))
            print(colored(f"  {ans_blue.text}", "blue", None, ["bold"]))
            if ans_yellow != "":
                print(colored(f"  {ans_yellow.text}", "yellow", None, ["bold"]))
            if ans_green != "":
                print(colored(f"  {ans_green.text}", "green", None, ["bold"]))
        elif option_no == 1:
            print(colored(f"  {ans_red.text}", "red", None, ["bold"]))
            print(colored(f"> {ans_blue.text}", "blue", None, ["bold"]))
            if ans_yellow != "":
                print(colored(f"  {ans_yellow.text}", "yellow", None, ["bold"]))
            if ans_green != "":
                print(colored(f"  {ans_green.text}", "green", None, ["bold"])) 
        if option_no == 2:
            print(colored(f"  {ans_red.text}", "red", None, ["bold"]))
            print(colored(f"  {ans_blue.text}", "blue", None, ["bold"]))
            if ans_yellow != "":
                print(colored(f"> {ans_yellow.text}", "yellow", None, ["bold"]))
            if ans_green != "":
                print(colored(f"  {ans_green.text}", "green", None, ["bold"]))
        elif option_no == 3:
            print(colored(f"  {ans_red.text}", "red", None, ["bold"]))
            print(colored(f"  {ans_blue.text}", "blue", None, ["bold"]))
            if ans_yellow != "":
                print(colored(f"  {ans_yellow.text}", "yellow", None, ["bold"]))
            if ans_green != "":
                print(colored(f"> {ans_green.text}", "green", None, ["bold"]))
    elif question_type == "TorF":
        if option_no == 0:
            print(colored(f"> {ans_red.text}", "blue", None, ["bold"])) # Yes, red is blue and blue is red. I know that.
            print(colored(f"  {ans_blue.text}", "red", None, ["bold"]))
        elif option_no == 1:
            print(colored(f"  {ans_red.text}", "blue", None, ["bold"]))
            print(colored(f"> {ans_blue.text}", "red", None, ["bold"]))
    elif question_type == "Multi":
        if option_no == 0:
            print(colored(f"> {ans_red.text}", "red", None, ["bold"]))
        elif option_no != 0:
            if 0 in picked_options:
                print(colored(">", "white", None, ["bold"]) ,colored(f"{ans_red.text}", "red", None, ["bold"]))
            else:
                print(colored(f"  {ans_red.text}", "red", None, ["bold"]))
        if option_no == 1:
            print(colored(f"> {ans_blue.text}", "blue", None, ["bold"]))
        elif option_no != 1:
            if 1 in picked_options:
                print(colored(">", "white", None, ["bold"]), colored(f"{ans_blue.text}", "blue", None, ["bold"]))
            else:
                print(colored(f"  {ans_blue.text}", "blue", None, ["bold"]))
        if option_no == 2 and ans_yellow != "":
            print(colored(f"> {ans_yellow.text}", "yellow", None, ["bold"]))
        elif option_no != 2 and ans_yellow != "":
            if 2 in picked_options:
                print(colored(">", "white", None, ["bold"]), colored(f"{ans_yellow.text}", "yellow", None, ["bold"]))
            else:
                print(colored(f"  {ans_yellow.text}", "yellow", None, ["bold"]))
        if option_no == 3 and ans_green != "":
            print(colored(f"> {ans_green.text}", "green", None, ["bold"]))
        elif option_no != 3 and ans_green != "":
            if 3 in picked_options:
               print(colored(">", "white", None, ["bold"]), colored(f"{ans_green.text}", "green", None, ["bold"]))
            else:
                print(colored(f"  {ans_green.text}", "green", None, ["bold"])) 
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
    

def getWinState():
    result_logo = driver.find_element(By.CSS_SELECTOR, "circle[cx='40']")
    if result_logo.get_attribute("fill") == "#66BF39":
        return True
    elif result_logo.get_attribute("fill") == "#F35":
        return False
    else:
        result_logo = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='partial-correct-answer']")
        return result_logo.text


correctMessages = ["Way to go, superstar!", "Amazing!", "Trust me, your oponents are jealous.", "One step closer to victory!", "Keep the flame lit!"]
wrongMessages = ["Don't worry, you'll get them next time!", "Never back down never what?", "Nice try!"]


print(colored("""
██╗░░██╗░█████╗░██╗░░██╗░█████╗░░█████╗░████████╗░░░░░░░█████╗░██╗░░░░░██╗
██║░██╔╝██╔══██╗██║░░██║██╔══██╗██╔══██╗╚══██╔══╝░░░░░░██╔══██╗██║░░░░░██║
█████═╝░███████║███████║██║░░██║██║░░██║░░░██║░░░█████╗██║░░╚═╝██║░░░░░██║
██╔═██╗░██╔══██║██╔══██║██║░░██║██║░░██║░░░██║░░░╚════╝██║░░██╗██║░░░░░██║
██║░╚██╗██║░░██║██║░░██║╚█████╔╝╚█████╔╝░░░██║░░░░░░░░░╚█████╔╝███████╗██║
╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░░╚════╝░░░░╚═╝░░░░░░░░░░╚════╝░╚══════╝╚═╝""", (100, 53, 173)))

print("Welcome to Kahoot-CLI! Made by @Aquaticsanti\n")

pin = ""

while True:
    try:
        if pin == "":
            pin = input("Input the game pin: ")
            if "https://kahoot.it" in pin: # For development purposes, this also takes copied links (I do not want to copy the pin manually)
                website = pin
            else:
                pin = pin.replace(" ", "")
                pin = int(pin)
                website = "https://kahoot.it"
    except ValueError:
            pin = input("That doesn't look like a number... Please input the game pin: ")
            if "https://kahoot.it" in pin: # For development purposes, this also takes copied links (I do not want to copy the pin manually)
                website = pin
            else:
                pin = int(pin)
                website = "https://kahoot.it"
    else:
        break

options = Options()
optionsToAdd = ["--disable-component-extensions-with-background-pages", "--disable-default-apps", "--disable-extensions", 
                "--disable-features=InterestFeedContentSuggestions", "--disable-features=Translate", "--mute-audio",
                "--no-default-browser-check", "--no-first-run", "--ash-no-nudges", "--disable-search-engine-choice-screen",
                "--propagate-iph-for-testing", "--disable-back-forward-cache", "--disable-features=BackForwardCache",
                "--disable-features=HeavyAdPrivacyMitigations", "--no-process-per-site", "--disable-background-networking",
                "--disable-component-update", "--disable-domain-reliability", "--disable-features=AutofillServerCommunication",
                "--disable-features=CertificateTransparencyComponentUpdater", "--disable-sync", "--metrics-recording-only",
                "--disable-features=OptimizationHints", "--single-process", "--headless=new"]
for arg in optionsToAdd:
    options.add_argument(arg)
driver = webdriver.Chrome(options=options)
driver.get(website)
driver.implicitly_wait(0.5)

if type(pin) == int: 
    pin_box = driver.find_element(by=By.NAME, value="gameId")
    pin_submit = driver.find_element(By.CSS_SELECTOR, ("button[type='submit']"))

    pin_box.send_keys(pin)
    pin_submit.click()

time.sleep(3)

lang = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='kahoot-settings__language-picker']")
lang.click()
langEN = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='option-with-value-en']")
langEN.click()

while True:
    if driver.current_url == "https://kahoot.it/join" or driver.current_url == "https://kahoot.it/namerator":
        break
    else:
        while True:
            try:
                pin = int(input("Uh oh, the pin is invalid. Input the game pin (no spaces): "))
            except ValueError:
                pin = int(input("That doesn't look like a number... Please input the game pin (no spaces): "))
            else:
                break
        pin_box.clear()    
        pin_box.send_keys(pin)
        pin_submit.click()

if driver.current_url == "https://kahoot.it/join":
    name_box = driver.find_element(by=By.NAME, value="nickname")
    name_submit = driver.find_element(By.CSS_SELECTOR, ("button[type='submit']"))

    validNickname = False
    nickname = input("What's your name? (Don't use your real name): ")
    while validNickname != True:
        if nickname == "":
            nickname = input("Uh oh, looks like your nickname is blank. Please choose a valid nickname (Don't use your real name): ")
        elif len(nickname) > 15:
            nickname = input("Uh oh, looks like your nickname is too long. Please choose a nickname with less than 15 characters (Don't use your real name): ")
        else:
            break

    name_box.send_keys(nickname)
    name_submit.click()
elif driver.current_url == "https://kahoot.it/namerator":
    nickname_old = ""
    print("This game uses a random name generator!")
    print("Press", colored("enter", None, None, ["italic"]), "to re-roll, and", colored("space", None, None, ["italic"]), "to select!")
    spins = 3
    while True:
        keypress = readkey()
        if keypress == key.ENTER:
            if spins > 0:
                spin_button = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='namerator-spin-button']")
                spins -= 1
                spin_button.click()
                while True:
                    print("Rolling...", end="\r")
                    try:
                        if spins > 0:
                            spin_button = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='namerator-spin-button']")
                            nickname = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='name-spinner-selected-name']")
                        else:
                            name_submit = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='namerator-continue-button']")
                            nickname = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='name-spinner-selected-name']")
                    except:
                        pass
                    else:
                        print("Your nickname is...", colored(nickname.text, None, None, ["bold"]))
                        print(colored(f"{spins} spins left", "dark_grey"))
                        break
            else:
                print("Uh oh, looks like there's no spins left! Please press", colored("space", None, None, ["italic"]), "to select.")
        elif keypress == key.SPACE:
            try:
                if nickname == "": # Basically check if nickname exists, without the user knowing
                    print("", end="\r")
            except NameError:
                print("Please roll once!")
            else:
                name_submit = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='namerator-continue-button']")
                nickname = nickname.text
                name_submit.click()
                break
        

while True:
    if driver.current_url == "https://kahoot.it/instructions":
        try:
            name_changed_alert = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='nickname-changed-notification']")
        except:
            print("You're in! See your name on the screen?")
        else:
            nickname = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='nickname']")
            nickname = nickname.text
            print(f"Your name has been changed to {nickname}")
        print(colored("Note: Reactions and avatars are not supported yet.", "dark_grey"))
        break
    elif driver.current_url == "https://kahoot.it/join":
        try:
            error_name_box = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='duplicate-name-error-notification']")
        except:
            continue
        else:
            nickname = input("Uh oh, that name's taken... Choose another one (Don't use your real name): ")
            name_box.clear()
            name_box.send_keys(nickname)
            name_submit.click()
            time.sleep(3)
    elif driver.current_url == "https://kahoot.it/gameblock":
        break
    elif driver.current_url == "https://kahoot.it/twoauth":
        try:
            if red_auth == "":
                print("", end="\r") # This is supposed to check if red_auth exists, AKA if it's the first time inputting the code
        except NameError:
            print("Looks like this game uses 2FA! Please input the combination shown on screen.")
            print(colored("r", "red"), "for", colored("red", "red"), end=", ")
            print(colored("b", "blue"), "for", colored("blue", "blue"), end=", ")
            print(colored("y", "yellow"), "for", colored("yellow", "yellow"), end=", ")
            print("and", colored("g", "green"), "for", colored("green", "green"))

            red_auth = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='two-factor-cards__triangle-button']")
            blue_auth = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='two-factor-cards__diamond-button']")
            yellow_auth = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='two-factor-cards__circle-button']")
            green_auth = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='two-factor-cards__square-button']")
        else:
            print("Please input the combination shown on screen.")
        combo = input()
        while True:
            if len(combo) > 4:
                combo = input("That combo is invalid, please try again: ")
            else:
                for char in combo:
                    if char not in ["r", "b", "y", "g", "R", "B", "Y", "G"]:
                        combo = input("That combo is invalid, please try again: ")
                        break
                if len(combo) == 4: # Not the best solution, but I guess it works?
                    break
        for char in combo:
            if char == "r" or char == "R":
                red_auth.click()
                time.sleep(0.25)
            elif char == "b" or char == "B":
                blue_auth.click()
                time.sleep(0.25)
            elif char == "y" or char == "Y":
                yellow_auth.click()
                time.sleep(0.25)
            elif char == "g" or char == "G":
                green_auth.click()
                time.sleep(0.25)
        time.sleep(0.5)
        if driver.current_url == "https://kahoot.it/twoauth":
            print("Uh oh, that combo was invalid.")
            

while driver.current_url != "https://kahoot.it/start":
    if driver.current_url == "https://kahoot.it/gameblock" or driver.current_url == "https://kahoot.it/":
        break
    else:
        pass

if driver.current_url == "https://kahoot.it/start":
    print("Get ready!")
    question_no = 1
elif driver.current_url == "https://kahoot.it/gameblock":
    question_no = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='question-index-counter']")
    question_no = int(question_no.text)
elif driver.current_url == "https://kahoot.it/":
    print("Uh oh, looks like you've been kicked out. Exiting...")
    os._exit(1) # Source - https://stackoverflow.com/a/49950466


while True: # This encapsulates the whole game logic.
    while driver.current_url != "https://kahoot.it/gameblock":
        pass

    cls() # Source - https://stackoverflow.com/a/684344, Clears entire CLI

    try:
        question_title = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='block-title']")
    except:
        question_title = None
    total_points_element = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='bottom-bar-score']")
    total_points = total_points_element.text

    try:
        question_type = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='question-type-heading-trueOrFalseTitle']")
    except:
        question_type = "Quiz"
    else:
        question_type = "TorF"
    
    try:
        submit_multi = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='multi-select-submit-button']")
    except:
        pass
    else:
        question_type = "Multi"

    print(colored(f"{nickname} - {total_points} points", "dark_grey"))
    if question_type == "Quiz" or question_type == "TorF":
        if question_title != None:
            print(f"Question {question_no} - {question_title.text}")
        else:
            print(f"Question {question_no}")
    elif question_type == "Multi":
        if question_title == None:
            print(f"Question {question_no}", colored(" (MULTIPLE CHOICE!)", None, None, ["bold"]))
        else:
            print(f"Question {question_no} - {question_title.text}", colored(" (MULTIPLE CHOICE!)", None, None, ["bold"]))

    ans_red = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='answer-0']")
    ans_blue = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='answer-1']")

    try:
        ans_yellow = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='answer-2']")
        amountOptions = 2
    except:
        ans_yellow = ""
        amountOptions = 1

    try:
        ans_green = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='answer-3']")
        amountOptions = 3
    except:
        ans_green = ""
        if ans_yellow != "":
            amountOptions = 2
    
    if question_type == "Multi":
        amountOptions += 1 # To account for the submit button
        picked_ans = []

    selected_ans = 0

    printSelectedAnswer(selected_ans, question_type)
    ranOutOfTime = False
    while True:
        if driver.current_url == "https://kahoot.it/answer/result":
            ranOutOfTime = True
            break
        keypress = readkey()
        if keypress == key.RIGHT or keypress == key.LEFT:
            continue
        print(f"\033[{amountOptions+2}A") # Moves cursor up x lines, Source - https://stackoverflow.com/a/72667369
        if keypress == key.UP:
            if driver.current_url == "https://kahoot.it/answer/result":
                ranOutOfTime = True
                break
            selected_ans -= 1
            if selected_ans < 0:
                selected_ans = amountOptions
            if question_type != "Multi":
                printSelectedAnswer(selected_ans, question_type)
            else:
                printSelectedAnswer(selected_ans, question_type, picked_ans)
        if keypress == key.DOWN:
            if driver.current_url == "https://kahoot.it/answer/result":
                ranOutOfTime = True
                break
            selected_ans += 1
            if selected_ans > amountOptions:
                selected_ans = 0
            if question_type != "Multi":
                printSelectedAnswer(selected_ans, question_type)
            else:
                printSelectedAnswer(selected_ans, question_type, picked_ans)
        if keypress == key.ENTER:
            if driver.current_url == "https://kahoot.it/answer/result":
                ranOutOfTime = True
                break
            if question_type == "Quiz" or question_type == "TorF":
                printSelectedAnswer(selected_ans, question_type)
                if selected_ans == 0:
                    ans_red.click()
                elif selected_ans == 1:
                    ans_blue.click()
                elif selected_ans == 2 and ans_yellow != "":
                    ans_yellow.click()
                elif selected_ans == 3 and ans_green != "":
                    ans_green.click()
                break
            elif question_type == "Multi":
                printSelectedAnswer(selected_ans, question_type, picked_ans)
                if selected_ans == 0:
                    ans_red.click()
                    if 0 not in picked_ans:
                        picked_ans.append(0)
                    elif 0 in picked_ans:
                        picked_ans.remove(0)
                elif selected_ans == 1:
                    ans_blue.click()
                    if 1 not in picked_ans:
                        picked_ans.append(1)
                    elif 1 in picked_ans:
                        picked_ans.remove(1)
                elif selected_ans == 2 and ans_yellow != "":
                    ans_yellow.click()
                    if 2 not in picked_ans:
                        picked_ans.append(2)
                    elif 2 in picked_ans:
                        picked_ans.remove(2)
                elif selected_ans == 3 and ans_green != "":
                    ans_green.click()
                    if 3 not in picked_ans:
                        picked_ans.append(3)
                    elif 3 in picked_ans:
                        picked_ans.remove(3)
                elif selected_ans == amountOptions:
                    if picked_ans == []:
                        continue
                    else:
                        submit_multi.click()
                        break


    while driver.current_url != "https://kahoot.it/answer/result":
        pass
    if ranOutOfTime == False:
        result = getWinState()
        if type(result) == bool:
            if result == True:
                points_increment = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='score-increment']")
                print(colored(f"Correct! {points_increment.text} points", "green", None, ["bold"]))
                print(correctMessages[random.randrange(len(correctMessages))])
            elif result == False:
                print(colored("Wrong...", "red", None, ["bold"]))
                print(wrongMessages[random.randrange(len(wrongMessages))])
        else:
            points_increment = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='score-increment']")
            points_increment = points_increment.text
            final_res = ""
            temp_res = ""
            save_line = False
            for char in result:
                temp_res += char
                if char == "/" and final_res == "":
                    save_line = True
                if char == "\n" and save_line == True:
                    final_res = temp_res
                    break
                elif char == "\n" and save_line == False:
                    temp_res = ""
            final_res = final_res.replace("\n", "")
            print(colored("Partially Correct", "light_blue", None, ["bold"]), f"- {final_res} right answers, for {points_increment} points")
    else:
        print(colored("You ran out of time...", "red", None, ["bold"]))
        print(wrongMessages[random.randrange(len(wrongMessages))])

    leaderboard_pos = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='player-rank']")
    try:
        nemesis = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='nemesis']")
    except:
        nemesis = ""
    else:
        nemesis_text = nemesis.text
        for char in nemesis_text:
            nemesis_text = nemesis_text.replace(char, "", 1)
            if char == "\n":
                break
    
    if nemesis != "":
        print(leaderboard_pos.text, nemesis_text)
    else:
        print(leaderboard_pos.text)

    while True: # Check if game has finished, or if there's another question
        if driver.current_url == "https://kahoot.it/gameblock":
            question_no += 1
            finished = False
            break
        elif driver.current_url == "https://kahoot.it/ranking":
            finished = True
            cls()
            break
        else:
            pass

    if finished == False:
        pass
    elif finished == True:
        break

try:
    non_podium = driver.find_element(By.TAG_NAME, "text")
except:
    non_podium = False

if non_podium != False:
    ranking = non_podium.text
    print(f"You scored {ranking}!")
else:
    print("Drumroll please...")
    time_slept = 0
    while True:
        try:
            podiumPlace = driver.find_element(By.CSS_SELECTOR, "path[fill='#FFC00A']")
        except:
            try:
                podiumPlace = driver.find_element(By.CSS_SELECTOR, "path[fill='#CCC']")
            except:
                try:
                    podiumPlace = driver.find_element(By.CSS_SELECTOR, "path[fill='#EB670F']")
                except:
                    time.sleep(1)
                    time_slept += 1
                    if time_slept > 7:
                        print("Uh oh, there seems to be an error. You're on the podium though, look at the screen!")
                        break
                else:
                    podiumPlace = 3
                    print("You got", colored("3rd place,", (205, 127, 50)), f"with a total of {total_points} points!")
                    break
            else:
                podiumPlace = 2
                print("You got", colored("2nd place,", (192, 192, 192)), f"with a total of {total_points} points!")
                break
        else:
            podiumPlace = 1
            print("You got", colored("1st place,", (255, 215, 0)), f"with a total of {total_points} points!")
            break

input()

