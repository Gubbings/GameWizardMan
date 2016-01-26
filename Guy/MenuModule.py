from easygui import *

def initMenu(imgPath):
    image = imgPath
    msg = "Game Title"
    choices = ["Play", "Tutorial", "Settings","Quit"]
    choice = buttonbox(msg, image=image, choices=choices)
    return choice
