# Kahoot_CLI

A python library for interacting with any kahoot quiz, as a participant!

# Features:
- [X] Joining a game
- [ ] Reactions
- [ ] Avatars
- [X] Answering single choice questions
- [X] Answering multiple choice questions
- [X] Answering True or False questions
- [X] Displaying points
- [X] Displaying ranking
- [X] Finishing a game
- [X] Error handling (this name is taken, pin is invalid, kicked out, etc.)
    
## Why would anyone need this, since this just uses Selenium?

Kahoot-CLI is designed in mind of devices that can't show a browser tab, like handheld devices. You can also adapt the UI to your liking.

>[!Note]
> This uses the Chrome webdriver, that has been trimmed down to use around 256mb of ram. I have not tested if it works with other browsers, or what happens if you don't have chrome installed.

# Usage
Kahoot_CLI has 2 modes, CLI and Module.

## CLI
To use the terminal mode, use:
    
    py -m kahoot_cli

You'll be prompted to input the session pin and your username, and you'll be in the session! _See your name on the screen?_

## Module

To import this as a module, you can use:
    
    from kahoot_cli import *

>[!Note]
> Yes, I know this isn't the best way to do it, but I haven't found a way that imports everything, that's not this.

For documentation, check out the [wiki](https://github.com/Aquaticsanti/kahoot_cli/wiki)!

# Requirements
- [A live kahoot you can join (duh)](https://create.kahoot.it/page/present)
- [Selenium](https://pypi.org/project/selenium/)
- [Termcolor](https://pypi.org/project/termcolor/)
- [Readchar](https://pypi.org/project/readchar/)

