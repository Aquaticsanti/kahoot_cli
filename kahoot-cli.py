from selenium import webdriver
from selenium.webdriver.common.by import By
from termcolor import colored
import time
import os
from readchar import readkey, key

def cls(): # Source - https://stackoverflow.com/a/684344
    os.system('cls' if os.name=='nt' else 'clear')

def printSelectedAnswer(option_no: int):
    if option_no == 0:
        print(colored(f"> {ans_red.text}", "red", None, ["bold"]))
        print(colored(f"  {ans_blue.text}", "blue", None, ["bold"]))
        if ans_yellow != "":
            print(colored(f"  {ans_yellow.text}", "yellow", None, ["bold"])) # type: ignore
        if ans_green != "":
            print(colored(f"  {ans_green.text}", "green", None, ["bold"])) # type: ignore
    elif option_no == 1:
        print(colored(f"  {ans_red.text}", "red", None, ["bold"]))
        print(colored(f"> {ans_blue.text}", "blue", None, ["bold"]))
        if ans_yellow != "":
            print(colored(f"  {ans_yellow.text}", "yellow", None, ["bold"])) # type: ignore
        if ans_green != "":
            print(colored(f"  {ans_green.text}", "green", None, ["bold"])) # type: ignore 
    if option_no == 2:
        print(colored(f"  {ans_red.text}", "red", None, ["bold"]))
        print(colored(f"  {ans_blue.text}", "blue", None, ["bold"]))
        if ans_yellow != "":
            print(colored(f"> {ans_yellow.text}", "yellow", None, ["bold"])) # type: ignore
        if ans_green != "":
            print(colored(f"  {ans_green.text}", "green", None, ["bold"])) # type: ignore
    elif option_no == 3:
        print(colored(f"  {ans_red.text}", "red", None, ["bold"]))
        print(colored(f"  {ans_blue.text}", "blue", None, ["bold"]))
        if ans_yellow != "":
            print(colored(f"  {ans_yellow.text}", "yellow", None, ["bold"])) # type: ignore
        if ans_green != "":
            print(colored(f"> {ans_green.text}", "green", None, ["bold"])) # type: ignore


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
    except ValueError:
        pin = int(input("That doesn't look like a number... Please input the game pin (no spaces): "))
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

time.sleep(3)

while True:
    if driver.current_url == "https://kahoot.it/instructions":
        print("You're in! See your name on the screen?")
        print(colored("Note: Reactions and avatars are not supported yet.", "dark_grey"))
        break
    elif driver.current_url == "https://kahoot.it/join":
        try:
            error_name_box = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='duplicate-name-error-notification']")
        except NoSuchElementException:
            break
        else:
            nickname = input("Uh oh, that name's taken... Choose another one (Don't use your real name): ")
            name_box.clear()
            name_box.send_keys(nickname)
            name_submit.click()
            time.sleep(3)


while driver.current_url != "https://kahoot.it/start":
    pass

print("Get ready!")

while driver.current_url != "https://kahoot.it/gameblock":
    pass
time.sleep(2)

cls() # Source - https://stackoverflow.com/a/684344, Clears entire CLI

question_title = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='block-title']")
question_no = 1

print(f"Question {question_no} - {question_title.text}")

ans_red = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='answer-0']")
ans_blue = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='answer-1']")

try:
    ans_yellow = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='answer-2']")
except NoSuchElementException:
    ans_yellow = ""

try:
    ans_green = driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='answer-3']")
except NoSuchElementException:
    ans_green = ""

selected_ans = 0

print(colored(f"  {ans_red.text}", "red", None, ["bold"]))
print(colored(f"  {ans_blue.text}", "blue", None, ["bold"]))
if ans_yellow != "":
    print(colored(f"  {ans_yellow.text}", "yellow", None, ["bold"]))
if ans_green != "":
    print(colored(f"  {ans_green.text}", "green", None, ["bold"]))


from readchar import readkey, key


while True:
    print("\033[5A") # Moves cursor up 5 lines, Source - https://stackoverflow.com/a/72667369
    keypress = readkey()
    if keypress == key.UP:
        selected_ans -= 1
        if selected_ans < 0:
            selected_ans = 3
        printSelectedAnswer(selected_ans)
    if keypress == key.DOWN:
        selected_ans += 1
        if selected_ans > 3:
            selected_ans = 0
        printSelectedAnswer(selected_ans)
    if keypress == key.ENTER:
        if selected_ans == 0:
            ans_red.click()
        elif selected_ans == 1:
            ans_blue.click()
        elif selected_ans == 2:
            ans_yellow.click() # type: ignore
        elif selected_ans == 3:
            ans_green.click() # type: ignore