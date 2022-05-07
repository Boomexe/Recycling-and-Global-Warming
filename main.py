import sys
from numpy import diff
import pygame
from pygame.locals import *
import random
import time
import os

cwd = os.getcwd()

assetsDir = os.path.join(cwd,'assets')
spritesDir = os.path.join(assetsDir, 'sprites')
soundsDir = os.path.join(assetsDir, 'sounds')

canOneImg = os.path.join(spritesDir,'crushed_can_1.png')
canTwoImg = os.path.join(spritesDir,'crushed_can_2.png')
canThreeImg = os.path.join(spritesDir,'crushed_can_3.png')
recycleBinImg = os.path.join(spritesDir,'recycle_bin.png')
foodImg = os.path.join(spritesDir,'unfinished_food_1.png')

trashItemImgs = [canOneImg, canTwoImg, canThreeImg, foodImg]


windowHeight, windowWidth = 800, 800
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((windowHeight, windowWidth))
pygame.display.set_caption("Youngwonks Recycling and Global Warming: REMASTERED")
pygame.display.set_icon(pygame.image.load(canOneImg))

endSound = pygame.mixer.Sound(os.path.join(soundsDir, 'end.wav'))
missItemSound = pygame.mixer.Sound(os.path.join(soundsDir, 'miss_item.wav'))
pickupItemSound = pygame.mixer.Sound(os.path.join(soundsDir, 'pickup_item.wav'))
selectSound = pygame.mixer.Sound(os.path.join(soundsDir, 'select.wav'))
gainLifeSound = pygame.mixer.Sound(os.path.join(soundsDir, 'gain_life.wav'))
missItemSpecialSound = pygame.mixer.Sound(os.path.join(soundsDir, 'miss_item_special.wav'))

# Colors
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
yellow = (255, 255,0)
black = (0, 0, 0)
colors = [red, green, blue, white, yellow]

# Vars
score = 0
lives = 10
difficulty = 6 # Startting difficulty
difficultyScaling = 15 # Seconds before difficulty increases
trashSize = 75 # Size of trash

gameStart = False
running = True
fps = 60
fpsClock = pygame.time.Clock()

trashList = []
specialTrashList = []
buttonList = []

def showText(msg, x, y, color, fontSize):
    font= pygame.font.SysFont('',fontSize)
    msg = font.render(msg,False,color)
    screen.blit(msg,(x,y))

def randomizer(numa, numb):
    return random.randint(numa, numb) == numa

def quit():
    pygame.quit()
    sys.exit()

def startGame():
    global gameStart
    gameStart = True

class character():
    def __init__(self, x, y, image, length, width):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.length = length
        self.width = width
        self.sprite = pygame.transform.scale(self.image, (self.length, self.width))
        
    def draw(self):
        screen.blit(self.sprite,(self.x,self.y))

class trashCharacter(character):
    def __init__(self, x, y, image, length, width, movespeed):
        super().__init__(x, y, image, length, width)
        self.moveSpeed = movespeed

    def move(self):
        self.y += self.moveSpeed
    
    def updateDifficulty(self):
        self.moveSpeed = difficulty

class buttonClass():
    def __init__(self, x, y, length, width, color, text, textColor, textFontSize, action):
        self.x = x
        self.y = y
        self.length = length
        self.width = width

        self.color = color
        self.text = text
        self.textColor = textColor
        self.textFontSize = textFontSize
        self.action = action
    
    def draw(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.length, self.width))
        showText(self.text, self.x, self.y, self.textColor, self.textFontSize)

    def onClick(self):
        self.action()

player = character(350, 725, recycleBinImg, 150, 75)
startButton = buttonClass(325, 375, 150, 50, green, 'Start', white, 80, lambda:startGame())
quitButton = buttonClass(325, 450, 150, 50, red, 'Quit', white, 80, lambda:quit())

buttonList.extend([startButton, quitButton])

startTime = time.time()
startTimeDisplay = time.perf_counter()

while running == True:
    fpsClock.tick(fps)

    # Drawing
    screen.fill(black)

    if gameStart == True:
        showText(f'Score: {score}', 0, 0, white, 40)
        showText(f'Lives: {lives}', 0, 25, white, 40)
        showText(f'Difficulty: {difficulty}', 0, 50, white, 40)
        showText(f'Timer: {int(time.perf_counter() - startTimeDisplay)}', 0, 75, white, 40)

        for trashItem in trashList:
            trashItem.draw()
            trashItem.move()

            if trashItem.x in range(player.x - trashItem.width, player.x + player.length) and trashItem.y in range(player.y - trashItem.width, player.y):
                trashList.remove(trashItem)
                score += 1
                pygame.mixer.Sound.play(pickupItemSound)
            
            if trashItem.y >= windowHeight:
                lives -= 1
                trashList.remove(trashItem)
                pygame.mixer.Sound.play(missItemSound)

                if lives <= 0:
                    running = False
        
        for specialTrashItem in specialTrashList:
            specialTrashItem.draw()
            specialTrashItem.move()
            if specialTrashItem.x in range(player.x - specialTrashItem.width, player.x + player.length) and specialTrashItem.y in range(player.y - specialTrashItem.width, player.y):
                specialTrashList.remove(specialTrashItem)
                score += 5
                lives += 1
                pygame.mixer.Sound.play(gainLifeSound)
            
            if specialTrashItem.y >= windowHeight:
                specialTrashList.remove(specialTrashItem)
                pygame.mixer.Sound.play(missItemSpecialSound)
        
        player.draw()
        player.x = pygame.mouse.get_pos()[0] - player.width

        if randomizer(1, 40):
            trashList.append(trashCharacter(random.randint(0, windowWidth - trashSize), 25, random.choice(trashItemImgs), trashSize, trashSize, difficulty))
        
        if randomizer(1, 200):
            specialTrashList.append(trashCharacter(random.randint(0, windowWidth - 100), 25, random.choice(trashItemImgs), int(trashSize/2), int(trashSize/2), difficulty * 2))

    else:
        for button in buttonList:
            button.draw()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == MOUSEBUTTONDOWN:
            for button in buttonList:
                if pygame.mouse.get_pos()[0] in range(button.x, button.x + button.length) and pygame.mouse.get_pos()[1] in range(button.y, button.y + button.width):
                    pygame.mixer.Sound.play(selectSound)
                    button.onClick()

    if time.time() - startTime >= difficultyScaling:
        difficulty += 1
        startTime = time.time()
    pygame.display.update()

screen.fill(black)
showText(f'You collected {score} pieces of trash.', 50, 350, white, 62)
showText(f'Time: {int(time.perf_counter() - startTimeDisplay)} seconds', 250, 450, white, 62)
pygame.mixer.Sound.play(endSound)

while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()