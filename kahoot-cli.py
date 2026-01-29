from selenium import webdriver
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
            print(colored(f"> SUBMIT", "white", None, ["bold"]))
        elif option_no != amountOptions:
            print(colored(f"  SUBMIT", "white", None, ["bold"]))
    

def getWinState():
    result_logo = driver.find_element(By.CSS_SELECTOR, "circle[cx='40']")

    if result_logo.get_attribute("fill") == "#66BF39":
        return True
    elif result_logo.get_attribute("fill") == "#F35":
        return False

correctMessages = ["Way to go, superstar!", "Amazing!", "Trust me, your oponents are jealous.", "One step closer to victory!", "Keep the flame lit!"]
wrongMessages = ["Don't worry, you'll get them next time!", "Never back down never what?", "", "Nice try!"]


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
            pin = input("Input the game pin (no spaces): ")
            if "https://kahoot.it" in pin: # For development purposes, this also takes copied links (I do not want to copy the pin manually)
                website = pin
            else:
                pin = int(pin)
                website = "https://kahoot.it"
    except ValueError:
            pin = input("That doesn't look like a number... Please input the game pin (no spaces): ")
            if "https://kahoot.it" in pin: # For development purposes, this also takes copied links (I do not want to copy the pin manually)
                website = pin
            else:
                pin = int(pin)
                website = "https://kahoot.it"
    else:
        break

driver = webdriver.Chrome()
driver.get(website)
driver.implicitly_wait(0.5)

if type(pin) == int: 
    pin_box = driver.find_element(by=By.NAME, value="gameId")
    pin_submit = driver.find_element(By.CSS_SELECTOR, ("button[type='submit']"))

    pin_box.send_keys(pin)
    pin_submit.click()

time.sleep(3)

while True:
    if driver.current_url == "https://kahoot.it/join":
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

name_box = driver.find_element(by=By.NAME, value="nickname")
name_submit = driver.find_element(By.CSS_SELECTOR, ("button[type='submit']"))

nickname = input("What's your name? (Don't use your real name): ")

name_box.send_keys(nickname)
name_submit.click()


while True:
    if driver.current_url == "https://kahoot.it/instructions":
        print("You're in! See your name on the screen?")
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


while driver.current_url != "https://kahoot.it/start":
    pass

print("Get ready!")



question_no = 1

while True: # This encapsulates the whole game logic.
    

    while driver.current_url != "https://kahoot.it/gameblock":
        pass
    time.sleep(1)

    cls() # Source - https://stackoverflow.com/a/684344, Clears entire CLI

    question_title = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='block-title']")
    total_points = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='bottom-bar-score']")

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

    print(colored(f"{nickname} - {total_points.text} points", "dark_grey"))
    if question_type == "Quiz" or question_type == "TorF":
        print(f"Question {question_no} - {question_title.text}")
    elif question_type == "Multi":
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

    while True:
        print(f"\033[{amountOptions+2}A") # Moves cursor up x lines, Source - https://stackoverflow.com/a/72667369
        keypress = readkey()
        if keypress == key.UP:
            selected_ans -= 1
            if selected_ans < 0:
                selected_ans = amountOptions
            if question_type != "Multi":
                printSelectedAnswer(selected_ans, question_type)
            else:
                printSelectedAnswer(selected_ans, question_type, picked_ans)
        if keypress == key.DOWN:
            selected_ans += 1
            if selected_ans > amountOptions:
                selected_ans = 0
            if question_type != "Multi":
                printSelectedAnswer(selected_ans, question_type)
            else:
                printSelectedAnswer(selected_ans, question_type, picked_ans)
        if keypress == key.ENTER:
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
                    picked_ans.append(0)
                elif selected_ans == 1:
                    ans_blue.click()
                    picked_ans.append(1)
                elif selected_ans == 2 and ans_yellow != "":
                    ans_yellow.click()
                    picked_ans.append(2)
                elif selected_ans == 3 and ans_green != "":
                    ans_green.click()
                    picked_ans.append(3)
                elif selected_ans == amountOptions:
                    submit_multi.click()
                    break


    while driver.current_url != "https://kahoot.it/answer/result":
        pass
    
    result = getWinState()

    points_increment = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='score-increment']")

    if result == True:
        print(colored(f"Correct! {points_increment.text} points", "green", None, ["bold"]))
        print(correctMessages[random.randrange(len(correctMessages))])
    elif result == False:
        print(colored("Wrong...", "red", None, ["bold"]))
        print(wrongMessages[random.randrange(len(wrongMessages))])

    question_no += 1
    
