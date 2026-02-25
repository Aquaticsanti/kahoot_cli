# Hey! Thanks for downloading my package. It means a lot to me. Also, this is the first real project I've ever made and published, so you might find some bugs. If you do, post an issue on GitHub, and I'll gladly take a look!
from .kahoot_cli import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
# Used by CLI
from termcolor import colored
import os
from readchar import readkey, key
import random