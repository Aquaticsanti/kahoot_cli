# Used by module
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
# Used by CLI
from termcolor import colored
import os
from readchar import readkey, key
import random

def cls(): # Source - https://stackoverflow.com/a/684344
    os.system('cls' if os.name=='nt' else 'clear')

class InvalidPinError(Exception):
    """Exception raised when the provided pin did not correspond to any current game, or link provided is not a link to kahoot.it"""

class InvalidNameError(Exception):
    """Exception raised when the provided nickname was deemed invalid. This can be due to 3 reasons:
        - The nickname was empty (This does not apply if a random name generator is used.)
        - The nickname was longer than 15 characters.
        - The nickname was taken."""

class InvalidFunctionUsage(Exception):
    """Exception raised when a function was improperly used.
        Example: Using Namerator() without a name generator being present."""

class NameratorError(Exception):
    """Errors related to the random name generator function. These are usually:
        - You haven't rolled at least once
        - You have zero rolls left"""

class KahootClient():
    def __init__(self) -> None: 
        """A KahootClient() object, used to interact with the actuall Kahoot Client.
        """
        return
    def JoinGame(self, pin: int | str) -> str:
        # Note: The pin can also be the kahoot.it invitation website. It will only accept a string if it contains "https://kahoot.it"
        """The joining function. Joins a game, and waits for a nickname.

        Args:
            pin (int | str): The pin to the corresponding game. This can also be a URL.
    
        Raises:
            InvalidPinError: If the provided pin was not a valid link, or it did not lead to a valid session.

        Returns:
            str: "ok" if the pin was correct, and the client is currently waiting for a nickname
            Note: It can also return "namerator" if a name generator is present.
        """

        self.pin = pin

        # Set up and launch selenium driver
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
        global _driver
        _driver = webdriver.Chrome(options=options)
        _driver.implicitly_wait(0.5)

        # Get webpage and join session
        if type(pin) == str:
            if "kahoot.it" in self.pin: 
                _driver.get(self.pin)
            else:
                raise InvalidPinError("The provided link does not lead to kahoot.it")
        elif type(pin) == int: 
            _driver.get("https://kahoot.it/")
            time.sleep(0.5)
            pin_box = _driver.find_element(by=By.NAME, value="gameId")
            pin_submit = _driver.find_element(By.CSS_SELECTOR, ("button[type='submit']"))

            pin_box.send_keys(self.pin)
            pin_submit.click()
        
        time.sleep(1.5)
        # Check if pin led to a valid session, raise InvalidPinError if not
        if _driver.current_url == "https://kahoot.it/join" or _driver.current_url == "https://kahoot.it/namerator":
            pass
        else:
            raise InvalidPinError(f"The pin ({self.pin}) does not lead to any current game.") 
        
        if _driver.current_url == "https://kahoot.it/join":
            return "ok"
        
        elif _driver.current_url == "https://kahoot.it/namerator":
            return "namerator"
        
        time.sleep(1)
        # Set language to English, to avoid missing elements due to language differences
        lang = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='kahoot-settings__language-picker']")
        lang.click()
        langEN = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='option-with-value-en']")
        langEN.click()

    def SetNickname(self, nickname: str) -> str:
        """Sets the nickname. This can only be used if JoinGame() was successful and no name generator is present

        Args:
            nickname (str): The desired nickname

        Raises:
            InvalidFunctionUsage: If this function was called without being able to set a nickname
            InvalidNameError: If the provided nickname is invalid (see InvalidNameError exception for reasons why).

        Returns:
            str: Basically a status code. It'll return **"ok"** if the nickname was valid, **"twoauth"** if 2FA is needed, **"started"** if the game joined has already started, and if the name was changed, it'll return the new name.
        """
        if _driver.current_url != "https://kahoot.it/join":
            raise InvalidFunctionUsage("SetNickname() was called without being able to set a nickname.")
        if len(nickname) > 15:
            raise InvalidNameError("The nickname provided is longer than 15 characters.")
        elif nickname == "":
            raise InvalidNameError("The nickname provided is empty.")
        self.nickname = nickname
        name_box = _driver.find_element(by=By.NAME, value="nickname")
        name_submit = _driver.find_element(By.CSS_SELECTOR, ("button[type='submit']"))
        
        name_box.send_keys(self.nickname)
        name_submit.click()
        time.sleep(1.5)
        if _driver.current_url == "https://kahoot.it/join":
            try:
                error_name_box = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='duplicate-name-error-notification']") # This variable is not made to be accessed, it was just made to check if the error box is there or not
            except:
                pass
            else:
                raise InvalidNameError("The provided nickname was taken.")
        elif _driver.current_url == "https://kahoot.it/instructions":
            nicknameElement = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='nickname']")
            if nicknameElement.text != nickname:
                self.nickname = nicknameElement.text  
                return nicknameElement.text
            else:
                return "ok"
        elif _driver.current_url == "https://kahoot.it/twoauth":
            return "twoauth"
        elif _driver.current_url == "https://kahoot.it/gameblock":
            return "started"
    def Namerator(self, roll: bool = False, keep: bool = False) -> str:
        """A function to interact with the random name generator, if there's one

        Args:
            roll (bool, optional): If it should roll a new nickname. Defaults to False.
            keep (bool, optional): If it should select the current nickname. Defaults to False.
        Note: These arguments are **exclusive**, meaning they cannot be used with each other.

        Raises:
            InvalidFunctionUsage: If this function was called without a name generator present, or both arguments are used.
            NameratorError: Errors related to the random name generator.

        Returns:
            str: The current nickname.
            Note: This will also be returned if "keep" is True.
        Note:
            This function keeps track of the remaining rolls by itself. You can access this by using "self.namerator_spins" You have a total of 3 rolls.
        """
        if _driver.current_url != "https://kahoot.it/namerator":
            raise InvalidFunctionUsage("Namerator() was used without a random name generator.")
        try:
            if _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='namerator-continue-button']") == "": # Basically check if the user has rolled before, without the user knowing
                pass
        except:
            global namerator_spins
            namerator_spins = 3
            self.namerator_spins = namerator_spins
        else:
            nickname = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='name-spinner-selected-name']")
            name_submit = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='namerator-continue-button']")
        finally:
            try:
                spin_button = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='namerator-spin-button']")
            except:
                pass
        if roll == True and keep == True:
            raise InvalidFunctionUsage("Namerator() was called with both flags set to True.")
        elif roll == True:
            if namerator_spins > 0:
                namerator_spins -= 1
                spin_button.click()
                while True:
                    try:
                        if namerator_spins > 0:
                            spin_button = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='namerator-spin-button']")
                            nickname = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='name-spinner-selected-name']")
                        else:
                            name_submit = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='namerator-continue-button']")
                            nickname = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='name-spinner-selected-name']")
                    except:
                        pass
                    else:
                        self.nickname = nickname.text
                        return nickname.text
            else:
                raise NameratorError("Tried to roll with 0 rolls left.")
        elif keep == True:
            try:
                if _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='namerator-continue-button']") == "": # Basically check if the user has rolled before, without the user knowing
                    pass
            except:
                raise NameratorError("Tried to keep a username without rolling first.")
            else:
                name_submit = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='namerator-continue-button']")
                self.nickname = nickname.text
                name_submit.click()
                return nickname
    def TwoAuth(self, order: list) -> bool:
        """A function to interact with the 2FA stage, if there is one.

        Args:
            order (list): A 4 item list, containing the code. The code should be:
                - "b" for blue
                - "r" for red
                - "g" for green
                - "y" for yellow.

        Raises:
            InvalidFunctionUsage: If function was called without a random name generator, or "order" doesn't follow the ettiquete above.

        Returns:
            bool: Returns "True" if the code was correct, and "False" if it wasn't.
        """
        if _driver.current_url != "https://kahoot.it/twoauth":
            raise InvalidFunctionUsage("TwoAuth function was called without 2FA needed.")
        
        try:
            if red_auth == "":
                print("", end="\r") # This is supposed to check if red_auth exists, AKA if it's the first time inputting the code
        except NameError:
            red_auth = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='two-factor-cards__triangle-button']")
            blue_auth = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='two-factor-cards__diamond-button']")
            yellow_auth = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='two-factor-cards__circle-button']")
            green_auth = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='two-factor-cards__square-button']")
        combo = order
        while True:
            if len(combo) > 4:
                raise InvalidFunctionUsage("The provided code is invalid.")
            else:
                for char in combo:
                    if char not in ["r", "b", "y", "g", "R", "B", "Y", "G"]:
                        raise InvalidFunctionUsage("The provided code is invalid.")
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
        if _driver.current_url == "https://kahoot.it/twoauth":
            return False
        elif _driver.current_url == "https://kahoot.it/instructions":
            return True
    def ClientState(self, fast: bool = False) -> str:
        """Returns where the client is (a question, podium, results, etc.). Note: The function waits 1 second before returning. This is to account for loading times. (This can be skipped by setting fast to True)

        Returns:
            str: Returns:
        - "Quiz" if in a question
        - "Start" if the game is just starting
        - "Res" if it's on the result page (of a question)
        - "End" if it's in the end of the game
        - "Wait" if it's on the question loading screen
        - "Lobby" if the game hasn't started yet
        - "Out" if you've been kicked out
        - "TwoAuth" if 2FA is required
        - "Namerator" if there's a random name generator present
        """
        if fast == False:
            time.sleep(1)
        if _driver.current_url == "https://kahoot.it/gameblock":
            return "Quiz"
        elif _driver.current_url == "https://kahoot.it/answer/result":
            return "Res"
        elif _driver.current_url == "https://kahoot.it/instructions":
            return "Lobby"
        elif _driver.current_url == "https://kahoot.it/":
            return "Out"
        elif _driver.current_url == "https://kahoot.it/getready":
            return "Wait"
        elif _driver.current_url == "https://kahoot.it/ranking":
            return "End"
        elif _driver.current_url == "https://kahoot.it/twoauth":
            return "TwoAuth"
        elif _driver.current_url == "https://kahoot.it/start":
            return "Start"
        elif _driver.current_url == "https://kahoot.it/namerator":
            return "Namerator"
    def GetQuestion(self) -> list:
        """Returns the current question type, title, and answers, if possible.

        Raises:
            InvalidFunctionUsage: If function was called outside a question

        Returns:
            list: A list of ["the question type", "the question title", question number (as an int), "top left answer", "top right answer", "bottom left answer", "bottom right answer"]
                
            The question types are:
        - "Quiz" for a regular quiz
        - "Multi" for a multiple choice quiz
        - "TorF" for a True or False quiz (This is separated from "Quiz" because in True or False, red and blue are swapped)

        Note: If the host hid the options to users, it'll return ["the question type", "", question number (as an int), "Red triangle", "Blue diamond", "Yellow circle", "Green square"]
        If it's a true or false question (with the answers hidden to users) it'll return ["(true or false)", "", "Blue diamond", "Red triangle"]
        """

        if _driver.current_url != "https://kahoot.it/gameblock":
            raise InvalidFunctionUsage("GetQuestion() was called outside a question.")
        
        # Question type identificator thingy
        try:
            question_type = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='question-type-heading-trueOrFalseTitle']")
        except:
            question_type = "Quiz"
        else:
            question_type = "TorF"
        
        try:
            submit_multi = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='multi-select-submit-button']") # This variable is not supposed to be used *here*, it should just be used to check the question type
        except:
            pass
        else:
            question_type = "Multi"
        
        # Title identification thingy
        try:
            question_title = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='block-title']")
        except:
            question_title = ""

        # Red and blue options identificator
        ans_red = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='answer-0']")
        ans_blue = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='answer-1']")

        # Check if yellow option exists
        try:
            ans_yellow = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='answer-2']")
            amountOptions = 2
        except:
            ans_yellow = ""
            amountOptions = 1

        # Check if green option exists
        try:
            ans_green = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='answer-3']")
            amountOptions = 3
        except:
            ans_green = ""
            if ans_yellow != "":
                amountOptions = 2
            else:
                amountOptions = 1

        # Checking question number
        question_no = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='question-index-counter']")
        question_no = int(question_no.text)

        # Returns
        if question_title == "":
            if amountOptions == 3:
                return [question_type, "", question_no, ans_red.text, ans_blue.text, ans_yellow.text, ans_green.text]
            elif amountOptions == 2:
                return [question_type, "", question_no, ans_red.text, ans_blue.text, ans_yellow.text]
            elif amountOptions == 1:
                return [question_type, "", question_no, ans_red.text, ans_blue.text]
        else:
            if amountOptions == 3:
                return [question_type, question_title.text, question_no, ans_red.text, ans_blue.text, ans_yellow.text, ans_green.text]
            elif amountOptions == 2:
                return [question_type, question_title.text, question_no, ans_red.text, ans_blue.text, ans_yellow.text]
            elif amountOptions == 1:
                return [question_type, question_title.text, question_no, ans_red.text, ans_blue.text]
    def AnswerQuestion(self, options: int | list):
        """Answers the current question.

        Args:
            options (int | list): The index of the desired response, or a list in the case of multiple choice questions.
                0 for top right, 1 for top left, 2 for bottom right, and 3 for bottom left.
                **Note**: For a regular quiz or true or false quiz, an interger is required. On the other hand, a multiple choice quiz requires a list, even if it's for one element.

        Raises:
            InvalidFunctionUsage: If the function was called outside a question, or the question was called incorrectly (for example, a list for a single choice question)
        """
        if _driver.current_url != "https://kahoot.it/gameblock":
                raise InvalidFunctionUsage("AnswerQuestion() was called outside a question.")
        
        # Question type identificator thingy
        try:
            submit_multi = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='multi-select-submit-button']")
        except:
            try:
                question_type = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='question-type-heading-trueOrFalseTitle']")
            except:
                question_type = "Quiz"
            else:
                question_type = "TorF"
        else:
            question_type = "Multi"
        
        
        
        # Options identificator thingy
        if type(options) == int:
            if 0 == options:
                ans_red = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='answer-0']")
            elif 1 == options:
                ans_blue = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='answer-1']")

            elif 2 == options:
                # Check if yellow option exists
                try:
                    ans_yellow = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='answer-2']")
                except:
                    ans_yellow = ""

            elif 3 == options:
                # Check if green option exists
                try:
                    ans_green = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='answer-3']")
                except:
                    ans_green = ""
        elif type(options) == list:
            if 0 in options:
                ans_red = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='answer-0']")
            elif 1 in options:
                ans_blue = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='answer-1']")

            elif 2 in options:
                # Check if yellow option exists
                try:
                    ans_yellow = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='answer-2']")
                except:
                    ans_yellow = ""

            elif 3 in options:
                # Check if green option exists
                try:
                    ans_green = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='answer-3']")
                except:
                    ans_green = ""


        if type(options) == list and question_type == "Quiz":
            raise InvalidFunctionUsage("A list was used to define the options of a regular quiz.")
        elif type(options) == list and question_type == "TorF":
            raise InvalidFunctionUsage("A list was used to define the options of a True or False quiz.")
        elif type(options) == int and question_type == "Multi":
            raise InvalidFunctionUsage("An interger was used to define the options of a Multiple Choice quiz.")

        if _driver.current_url == "https://kahoot.it/answer/result":
            return
        if question_type == "Quiz" or question_type == "TorF":
            if options == 0:
                ans_red.click()
            elif options == 1:
                ans_blue.click()
            elif options == 2 and ans_yellow != "":
                ans_yellow.click()
            elif options == 3 and ans_green != "":
                ans_green.click()
            return
        elif question_type == "Multi":
            if 0 in options:
                ans_red.click()
            if 1 in options:
                ans_blue.click()
            if 2 in options and ans_yellow != "":
                ans_yellow.click()
            if 3 in options and ans_green != "":
                ans_green.click()
            submit_multi.click()
            return
    def GetResult(self) -> str | list:
        """Checks the result of the latest question, and returns the result and points (if possible).

        Raises:
            InvalidFunctionUsage: If the function was called outside the results page.

        Returns:
            str|list: If you haven't won, it'll return a string. It will be either:
        - "Lose" (if you've lost)
        - "NoTime" (if you ran out of time)
                    However, if you have won, it will return a list, containing: ["Win", "+(the amount of points you've gained)"]
                    (If it's partially correct, it'll return ["(correct)/(total)", "+(the amount of points you gained"])
        """
        if _driver.current_url != "https://kahoot.it/answer/result":
            raise InvalidFunctionUsage("GetResult() was called outside the results page.")
        try:
            ranOutOfTime = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='time-up-answer']")
        except:
            ranOutOfTime = False
        else:
            ranOutOfTime = True
        if ranOutOfTime == False:
            result_logo = _driver.find_element(By.CSS_SELECTOR, "circle[cx='40']")
            if result_logo.get_attribute("fill") == "#66BF39":
                result = "Win"
                points_increment = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='score-increment']")
            elif result_logo.get_attribute("fill") == "#F35":
                result = "Lose"
            else:
                result_logo = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='partial-correct-answer']")
                result = result_logo.text
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
                result = final_res
            if result == "Lose" or result == "NoTime":
                return result
            else:
                return [result, points_increment.text]
        else:
            return "NoTime"
    def GetLeaderboardPos(self) -> list:
        """Returns the current leaderboard rank, and nemesis (if possible)

        Raises:
            InvalidFunctionUsage: Raised when this function was called outside the results page.

        Returns:
            list: If the user is not in the podium, it'll return [(position as int), "x points behind nemesis"].
            If the user IS in the podium, it'll return ["Podium"]
        """
        if _driver.current_url != "https://kahoot.it/answer/result":
            raise InvalidFunctionUsage("GetLeaderboardPos() was called outside the results page.")
        
        leaderboard_pos = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='player-rank']")
        try:
            nemesis = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='nemesis']")
        except:
            nemesis = ""
        else:
            nemesis_text = nemesis.text
            leaderboard_pos_int = ""
            for char in nemesis_text:
                nemesis_text = nemesis_text.replace(char, "", 1)
                if char == "\n":
                    break
        for char in leaderboard_pos.text:
            if char in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                leaderboard_pos_int += char
        try:
            leaderboard_pos_int = int(leaderboard_pos_int)
        except:
            pass
        if nemesis != "":
            return [leaderboard_pos_int, nemesis_text]
        else:
            return ["Podium"]
    def GetPoints(self) -> int:
        """Returns the total amount of points.  
        _(for returning the point increment, see GetResult())_

        Raises:
            InvalidFunctionUsage: If this function was called outside a game.

        Returns:
            int: The total amount of points.
        """
        if _driver.current_url in ["https://kahoot.it/", "https://kahoot.it/join"]:
            raise InvalidFunctionUsage("GetPoints() was called outside a game.")
        total_points_element = _driver.find_element(By.CSS_SELECTOR, "[data-functional-selector='bottom-bar-score']")
        total_points = int(total_points_element.text)
        return total_points
    def GetFinalRanking(self) -> int:
        """Returns the final ranking, as an interger.
        - If the position is not in the podium, it will return a number from 4 to the total amount of players (inclusive)
        - If the position is in the podium, but hasn't been shown yet it'll return 0.
        - If the position is in the podium, and has been shown, it'll return a number from 1 to 3 (inclusive)

        Raises:
            InvalidFunctionUsage: If the function was called outside the ranking phase

        Returns:
            int: The ranking.
        """
        if _driver.current_url != "https://kahoot.it/ranking":
            raise InvalidFunctionUsage("GetFinalRanking() was called outside ranking phase.")
        try:
            non_podium = _driver.find_element(By.TAG_NAME, "text")
        except:
            non_podium = False

        if non_podium != False:
            ranking = non_podium.text
            final_str = ""
            for char in ranking:
                if char in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
                    final_str += char
                else:
                    pass
            return final_str
        else:
            try:
                podiumPlace = _driver.find_element(By.CSS_SELECTOR, "path[fill='#FFC00A']")
            except:
                try:
                    podiumPlace = _driver.find_element(By.CSS_SELECTOR, "path[fill='#CCC']")
                except:
                    try:
                        podiumPlace = _driver.find_element(By.CSS_SELECTOR, "path[fill='#EB670F']")
                    except:
                        return 0
                    else:
                        return 3
                else:
                    return 2
            else:
                return 1
    

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

    print("Welcome to Kahoot-CLI! Made by @Aquaticsanti\n")

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

