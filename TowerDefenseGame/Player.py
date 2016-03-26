#This is a simple module used to hold the players information
#it contains information such as resources and health
health = 100
gold = 25                

def changeHealth(delta):
    global health
    health += delta

def changeGold(delta):
    global gold
    gold += gold