### Proteeti Sinha
### Andrew ID: proteets
### Term Project
### Level 1 

from tkinter import *
import random, math, copy 
import time
from tkinter import messagebox 
# Classes: Button, Player, Spell, Platform, Enemy, Coin

### Button Class 

class Button(object):
    def __init__(self, x1, x2, y1, y2, width, height, text = None):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.width = width
        self.height = height
        self.text = text
        
    def create(self, canvas):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill = "red")
        canvas.create_text(self.x1 + self.width//2, self.y1 + self.height//2, text = self.text)
        
    def buttonPress(self, clickX, clickY):
        if clickX >= self.x1 and clickX <= self.x2:
            if clickY >= self.y1 and clickY <= self.y2:
                return True
        else:
            return False 
            
### Player class 

class Player(object):
    def __init__(self, posX, posY, speed, scrollX):
        # a player has a position, speed and direction of movement
        self.posX = posX
        self.posY = posY
        self.speed = 10
        self.size = 40
        self.angle = 0
        self.scrollX = scrollX
        self.scrollMargin = 40
        self.jumping = False 
        self.onGround = True 
        self.jumps = 30
        self.image1 = PhotoImage(file = "harryflying.gif")
        self.image2 = PhotoImage(file = "ron.gif")
        self.image3 = PhotoImage(file = "hermione.gif")
        self.image5 = PhotoImage(file = "dumbledore.gif")
        self.image4 = PhotoImage(file = "hagrid.gif")
    
    # draws the player    
    def drawPlayer(self, canvas):
        contentsRead = readFilePlayer("player1.txt")
        character = contentsRead
        if character == "data.harry":
            canvas.create_image(self.posX - self.scrollX - 20, self.posY, \
        image = self.image1)
        if character == "data.ron":
            canvas.create_image(self.posX - self.scrollX - 20, self.posY, \
        image = self.image2)
        if character == "data.hermione":
            canvas.create_image(self.posX - self.scrollX - 20, self.posY, \
        image = self.image3)
        if character == "data.hagrid":
            canvas.create_image(self.posX - self.scrollX - 20, self.posY, \
        image = self.image4)
        if character == "data.dumbledore":
            canvas.create_image(self.posX - self.scrollX - 20, self.posY, \
        image = self.image5)
    
    
    def movePlayer(self, dx, dy):
        self.posY += dy
        self.posX += dx
        if (self.posX < self.scrollX + self.scrollMargin):
            self.scrollX = self.posX - self.scrollMargin
        if self.posX > (self.scrollX - self.scrollMargin + 500): # data.width = 600 
            self.scrollX = self.posX  + self.scrollMargin - 500 


    def run(self):
        self.posX += 5
        if (self.posX < self.scrollX + self.scrollMargin):
            self.scrollX = self.posX - self.scrollMargin
        if self.posX > (self.scrollX - self.scrollMargin + 500): # data.width = 600
            self.scrollX = self.posX - 500 + self.scrollMargin
        
    def makeReducioSpell(self, cx, cy, speed, direction):
        # makes a reducing spell 
        x = self.posX + self.size/2 - self.scrollX
        y = self.posY + self.size/2
        self.speed = 20
        self.direction = direction
        return Spell(x, y, self.angle, self.speed, [0,1])
    
    def makeStupefySpell(self, cx, cy, speed, direction):
        # makes a spell which stupefies opponent
        x = self.posX + self.size/2 - self.scrollX 
        y = self.posY + self.size/2
        self.speed = 20
        self.direction = direction
        return Spell(x, y, self.angle, self.speed, [0,1])
    
    def makeKedavraSpell(self, cx, cy, speed, direction):
        # makes a spell which stupefies opponent
        x = self.posX + self.size/2 - self.scrollX
        y = self.posY + self.size/2
        self.speed = 20
        self.direction = direction
        return Spell(x, y, self.angle, self.speed, [0,1])
        
    def collidesWithCoin(self, other):
        # checks if player gets coin 
        if (not isinstance(other, Coin)):
            return False 
        else:
            dist = ((other.x - self.posX)**2 + (other.y - self.posY)**2)**0.5 
            return dist < other.radius + self.size/2     
            
    def jump(self):
        # makes the player jump 
        self.jumping = True 
        self.posY -= self.jumps
        self.posX += 10
         
    def falls(self, other):
        if not isinstance(other, Platform):
            return False
        else:
            if self.posX > other.x1 and self.posX < other.x2:
                if self.posY + 20 > other.y1:
                    return True
 
### Platform class

class Platform(object):
    def __init__(self, x1, y1, x2, y2):
        # a platform has a position 
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2 
        
    def draw(self, canvas, scrollX):
        canvas.create_rectangle(self.x1 - scrollX, self.y1, self.x2 - scrollX,\
         self.y2, \
        fill = "lightskyblue", width = 0 )
        

### Spell class   
     
class Spell(object):
    def __init__(self, cx, cy, angle, speed, direction):
        # a spell has a position, speed and size 
        self.cx = cx
        self.cy = cy
        self.r = 10 
        self.angle = angle
        self.speed = speed
        self.direction = direction 
        
    def drawSpell(self, canvas, color = "cyan"):
        # draws the spell
        canvas.create_oval(self.cx - self.r, self.cy - self.r, 
                           self.cx + self.r, self.cy + self.r,
                           fill=color, width = 0)
                           
    def moveSpell(self):
        # makes the spell move 
        self.cx += self.speed * self.direction[1]
        self.cy += self.speed*self.direction[0]
        
        
    # from hw11 helper function collidesWithAsteroid    
    def collidesWithEnemy(self, other):
        # checks if spells collides with enemy 
        if(not isinstance(other, Enemy)): # Other must be an Enemy
            return False
        else:
            # distance formula 
            dist = ((other.cx - self.cx)**2 + (other.cy - self.cy)**2)**0.5
            return dist < self.r + other.r 
    
class Stupefy(Spell):
    def __init__(self, cx, cy, speed, direction):
        # inherits
        super().__init__(cx, cy, speed, direction)
        
    def drawSpell(self, canvas):
        # inherits 
        super().drawSpell(canvas, color = "red")
        
    def moveSpell(self):
        # makes the spell move 
        self.cx += math.cos(math.radians(self.angle))*self.speed
        self.cy -= math.sin(math.radians(self.angle))*self.speed

class Reducio(Spell):
    def __init__(self, cx, cy, speed, direction):
        super().__init__(cx, cy, speed, direction)
        
    def drawSpell(self, canvas):
        super().drawSpell(canvas, color = "purple")
        
    
class AvadaKedavra(Spell):
    def __init__(self, cx, cy, speed, direction):
        super().__init__(cx, cy, speed, direction)
        
    def drawSpell(self, canvas):
        super().drawSpell(canvas, color = "lawngreen")

### Enemy class

class Enemy(object):
    def __init__(self, cx, cy, r, speed, direction):
        # an enemy has a position, speed, radius and direction
        self.cx = cx
        self.cy = cy
        self.r = r
        self.speed = speed
        self.direction = direction 
        self.reduce = 10
    
    # draws the enemy
    def drawEnemy(self, canvas, color = "orange"):
        canvas.create_oval(self.cx - self.r, self.cy - self.r,
                           self.cx + self.r, self.cy + self.r,
                           fill=color)
    def moveEnemy(self):
        # makes the enemy move
        self.cy += self.speed* self.direction[0]
        self.cx += self.speed * self.direction[1]
            
    def reactToStupefyHit(self):
        # reaction to stupefy spell
        self.speed = 0 # speed becomes 0
    
    def reactToReducioHit(self):
        # reaction to reducio spell 
        self.r -= self.reduce

# subclass dragon
class Dragon(Enemy):
    def __init__(self, cx, cy, r, speed, direction):
        # inherit
        super().__init__(cx, cy, r, speed, direction)
    
    def drawEnemy(self, canvas):
        # inherit, different color
        super().drawEnemy(canvas, color="green4")    
    # inherits reactions to spells
        
# subclass spider     
class GiantSpider(Enemy):
    def __init__(self, cx, cy, r, speed, direction):
        super().__init__(cx, cy, r, speed, direction)
        # giant spiders like Aragog become less giant
        
    def drawEnemy(self, canvas):
        # inherit, different color
        super().drawEnemy(canvas, color="orange")   

### Coins class

class Coin(object):
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        
    def draw(self, canvas, scrollX):
        canvas.create_oval(self.x - self.radius - scrollX, self.y - self.radius, \
        self.x + self.radius - scrollX, self.y + self.radius, fill = "yellow",\
         width = 2)
        

### some helper functions for redrawAll 

def playerCrossesBounds(data):
    # if a player goes on the other players screen, they die 
    if data.player1.posY + 30 > data.height/2:
        data.player1Dead = True 
    elif data.player2.posY - 30 < data.height/2:
        data.player2Dead = True 

def player1Wins(canvas, data):
    # if player 1 wins...
    dist = 100
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "purple")
    canvas.create_rectangle(dist/2, dist/2, data.width - dist/2, \
    data.height - dist/2, fill = "blue")
    canvas.create_rectangle(dist, dist, data.width - dist, data.height - dist, \
    fill = "slateblue1")
    canvas.create_text(data.width/2, data.height*3/4, \
    text = "Press h to go to level 2!", font = "ComicSansMS 30 bold")
    canvas.create_image(data.width/2, data.height/2, image = data.win1)
    canvas.create_text(data.width/2, data.height/2 + 100, \
    text = "Player 1: Your score was " + str(data.score1), font = "ComicSansMS 30")
    canvas.create_text(data.width/2, data.height/2 + 130, \
    text = "Player 2: Your score was " + str(data.score2), font = "ComicSansMS 30")
    canvas.create_text(data.width/2, data.height/2 + 40, \
    text = "Press space to see recent scores!")
    
def player2Wins(canvas, data):
    # if player 2 wins...
    dist = 100
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "purple")
    canvas.create_rectangle(dist/2, dist/2, data.width - dist/2, \
    data.height - dist/2, fill = "blue")
    canvas.create_rectangle(dist, dist, data.width - dist, data.height - dist,\
    fill = "slateblue1")
    canvas.create_image(data.width/2, data.height/2, image = data.win2)
    canvas.create_text(data.width/2, data.height/2 + 100, \
    text = "Player 1: Your score was " + str(data.score1), font = "ComicSansMS 30")
    canvas.create_text(data.width/2, data.height/2 + 130, \
    text = "Player 2: Your score was " + str(data.score2), font = "ComicSansMS 30")
    canvas.create_text(data.width/2, data.height/2 + 40, \
    text = "Press space to see recent scores!")

def isPaused(canvas, data):
    # if the game is paused 
    data.player1.drawPlayer(canvas)
    data.player2.drawPlayer(canvas)
    canvas.create_rectangle(data.width/2 - 150, data.height/2 - 150, \
    data.width/2 + 150, data.height/2 + 150, fill = "blue")
    canvas.create_text(data.width/2, data.height/2, text = "PAUSED", \
    font = "Arial 40 bold")
    canvas.create_text(data.width/2, data.height/2 + 50, \
    text = "Cast spells to kill enemies!", font = "ComicSansMS 20 bold")
    
def drawScore(canvas, data):
    # player 1 
    canvas.create_text(data.width/4, 20, anchor="s", \
    fill="grey4", font="Arial 16 bold", text="Player 1: " + str(data.score1))
    # player 2
    canvas.create_text(data.width*3/4, 20, anchor = "s", fill = "grey4", \
    font = "Arial 16 bold", text = "Player 2: " + str(data.score2))

def drawTrees(canvas, data):
    # draws trees at intervals
    distance = 10 
    while distance < (data.worldWidth):
        if distance%500 == 0 and distance != 0:
            canvas.create_image(distance - data.scrollX, data.height/3, \
            image = data.treeImage)
            canvas.create_image(distance - data.scrollX, data.height*5/6, \
            image = data.treeImage)
        distance += 10

def finishPole(canvas, data, scrollX):
    # draws the finish line 
    canvas.create_image(1900 - scrollX, data.height/3 - 40, \
    image = data.finishPic)
    canvas.create_image(1900 - scrollX, data.height*5/6 - 40, \
    image = data.finishPic)
    
def drawLives(canvas, data):
    # draws lives remaining for each player 
    canvas.create_text(data.width/4 - 80, 20, anchor="s", \
    fill="grey4", font="Arial 16 bold", text="Lives: " + str(data.lives1))
    canvas.create_text(data.width*3/4 + 80, 20, anchor="s", \
    fill="grey4", font="Arial 16 bold", text="Lives: " + str(data.lives2))


### Highscore stuff 

def recentScores(canvas, data):
    if data.player1Dead == True:
        name = input("Player 2, please enter your name")
        score = str(data.score2)
        stuff = name + ": " + score + "\n"
        writeFileScore("recent.txt", stuff)
        dataFile = readFileScore("recent.txt")
        dataFile = dataFile.split("\n") # creates the list 
        dataFile = dataFile[-1::-1]
        for elem in range(len(dataFile)):
            canvas.create_text(data.width/2, data.height/2 + elem*20,\
            text = dataFile[elem])
    elif data.player2Dead == True:
        name = input("Player 1, please enter your name")
        score = str(data.score1)
        stuff = name + ": " + score + "\n"
        writeFileScore("recent.txt", stuff)
        dataFile = readFileScore("recent.txt")
        dataFile = dataFile.split("\n") # creates the list 
        dataFile = dataFile[-1::-1] # reverses the list 
        for elem in range(len(dataFile)):
            canvas.create_text(data.width/2, data.height/2 + elem*20,\
            text = dataFile[elem])
        


### Animation stuff
    
def readFilePlayer(path):
    with open(path, "rt") as f:
        return f.read()  
          
def writeFilePlayer1(path, contents):
    with open(path, "wt") as f:
        f.write(contents)
        
def init1(data):
    # initialises values 
    data.scrollX = 0
    data.finishPic = PhotoImage(file = "finish.gif")
    pInitialX = 40 - data.scrollX # initial position x coordinate
    data.paused = False
    data.worldWidth = 5* data.width
    data.worldHeight = data.height
    pInitialY = data.height//4 # initial position y coordinate 
    data.player1 = Player(pInitialX - data.scrollX, pInitialY, 10, 0)
    data.player2 = Player(40 - data.scrollX, 3*data.height//4, 10, 0)
    data.gameOver = False 
    # initialising spells for both players 
    data.reducioSpell = data.player1.makeReducioSpell(data.width//2 - \
    data.scrollX, data.height//2, 20, [0,1])
    data.reducioSpell2 = data.player2.makeReducioSpell(data.width//2 - \
    data.scrollX, data.height//2, 20, [0,1])
    data.kedavraSpell = data.player1.makeKedavraSpell(data.width//2 - \
    data.scrollX, data.height//2, 20, [0,1])
    data.kedavraSpell2 = data.player2.makeKedavraSpell(data.width//2 - \
    data.scrollX, data.height//2, 20, [0,1])
    # photos 
    data.background = PhotoImage(file = "bg.gif")
    data.congrats = PhotoImage(file = "congrats.gif")
    data.paused = PhotoImage(file = "pause.gif")
    data.pImage = PhotoImage(file = "harryflying.gif")
    data.ron = PhotoImage(file = "ron.gif")
    data.hermione = PhotoImage(file = "hermione.gif")
    data.dumbledore = PhotoImage(file = "dumbledore.gif")
    data.hagrid = PhotoImage(file = "hagrid.gif")
    data.win1 = PhotoImage(file = "player1wins.gif")
    data.win2 = PhotoImage(file = "player2wins.gif")
    # data.seconds = 30
    data.timerCalls =  0
    data.score1 = 0 
    data.score2 = 0
    data.ground1 = data.height/3
    data.ground2 = data.height*5/6
    data.scrollX = 0
    data.shrubs = []
    data.scrollMargin = 40
    data.spells = []
    data.treeImage = PhotoImage(file = "tree.gif")
    data.player1Dead = False
    data.player2Dead = False 
    data.player1Won = False
    data.player2Won = False
    # lives for player 1 and 2 
    data.lives1 = 3
    data.lives2 = 3
    data.timePassed = 0 
    data.tie = False 
    # create pre existing enemies 
    # initial enemy parameters:
    startPosX = [400, 490, 830, 1060, 1500, 1550, 1700, 1900, 1200, 1000, \
    1670, 1340]
    startPosY = [25, 50, 100, 160, 230, 190, 340, 410, 390, 500, 540, 470]
    randomEnemy = random.choice([Dragon, Enemy, GiantSpider])
    data.enemies = []
    # making platforms 
    data.platforms = []
    platformX1 = [370, 700, 870, 1800]
    platformX2 = [570, 900, 1070, 2000]
    
    for i in range(len(platformX1)):
        # creates platforms for both players, separately    
        data.platform1 = Platform(platformX1[i], data.ground1, platformX2[i], \
        data.height/2)
        data.platforms.append(data.platform1)
        data.platform2 = Platform(platformX1[i], data.ground2, platformX2[i], \
        data.height)
        data.platforms.append(data.platform2)
        
    data.coins = []
    possX = [200, 600, 1230, 1400, 2000, 1780, 890, 2310, 1900, 340]
    possY = [30, 70, 130, 200, 265, 350, 400, 470, 520, 570 ]
    radius = 10
    for i in range(len(possX)):
        coin = Coin(possX[i], possY[i], radius)
        data.coins.append(coin)
    data.over = PhotoImage(file ="gameover.gif")
    # creates initial enemies 
    for i in range(len(startPosX)):
        randomE = randomEnemy(startPosX[i] - data.scrollX, startPosY[i], 20, \
        2, [0,-1])
        data.enemies.append(randomE)
            
def mousePressed1(event, data):
    pass
    
def keyPressed1(event, data):
    # Controller 
    speed = 20
    # scroll edge cases 
    if data.player1.posX < data.scrollX + data.scrollMargin:
        data.scrollX = data.player1.posX - data.scrollMargin 
    
    if data.player1.posX > data.scrollX + data.width - data.scrollMargin:
        data.scrollX = data.player1.posX + data.scrollMargin - data.width
        
    if data.player2.posX < data.scrollX + data.scrollMargin:
        data.scrollX = data.player2.posX - data.scrollMargin
        
    if data.player2.posX > data.scrollX + data.width - data.scrollMargin:
        data.scrollX = data.player2.posX + data.scrollMargin - data.width
    
    if event.keysym == "Up":
        data.player1.movePlayer(0, -15)
        
    if event.keysym == "Down":
        data.player1.movePlayer(0, 15)
        
    if event.keysym == "Right":
        data.player1.movePlayer(15, 0)
        
    if event.keysym == "Left":
        data.player1.movePlayer(-15, 0)
        
    if event.keysym == "a":
        data.player2.movePlayer(-15, 0)
        
    if event.keysym == "d":
        data.player2.movePlayer(15, 0)
        
    if event.keysym == "w":
        data.player2.movePlayer(0, -15)
        
    if event.keysym == "s":
        data.player2.movePlayer(0, 15)
        
    if data.paused == True:
        # unpause 
        if event.keysym == "space":
            data.paused = False 

    if event.keysym == "j":
        data.player1.jump()
        
    if event.keysym == "z":
        data.player2.jump()
 
        
    # spells for player 1: 
    # letters have been chosen so as to allow both players to play 
    # without their fingers tangling
    if event.keysym == "m":
          # makes reducio spell 
        data.reducioSpell = data.player1.makeReducioSpell(data.width//2 - \
        data.scrollX, 
        data.height//2, speed, [0,1])
        data.spells.append(data.reducioSpell)

    if event.keysym == "k":
        # avada kedavra spell 
        data.kedavraSpell = data.player1.makeKedavraSpell(data.width//2- \
        data.scrollX,
        data.height//2, speed, [0,1])
        data.spells.append(data.kedavraSpell)
        
    # spells for player 2:
    if event.keysym == "q":
        # avada kedavra spell player 2 
        data.kedavraSpell2 = data.player2.makeKedavraSpell(data.width//2 - \
        data.scrollX, data.height//2, speed, [0,1])
        data.spells.append(data.kedavraSpell2)
        
    if event.keysym == "r":
        # reducio spell player 2
        data.reducioSpell2 = data.player2.makeReducioSpell(data.width//2, \
        data.height//2, speed, [0,1])
        data.spells.append(data.reducioSpell2)
        
    elif event.keysym == "p":
        # pause 
        data.paused = True 
        
   
def timerFired1(data):
    data.timerCalls += 1
    # moves spells
    for spell in data.spells:
        spell.moveSpell()
    playerCrossesBounds(data)            
    # both players are moving 
    data.player1.run()
    data.player2.run()
    
    # jumping and gravity stuff 
    if data.player1.jumping == True and data.player1.posY < (data.ground1 - 20):
        # force of gravity acts
        data.player1.posY += 5
        
    if data.player2.jumping == True and data.player2.posY < (data.ground2- 20):
        data.player2.posY += 5

    # moves enemies 
    for enemy in data.enemies:
            enemy.moveEnemy() 
             
  
    for spell in data.spells:
        for enemy in data.enemies:
            # reactions to various spells 
            if spell.collidesWithEnemy(enemy):
                if spell == data.reducioSpell:
                    enemy.reactToReducioHit()
                    data.spells.remove(spell)
                    if enemy.r < 5:
                        data.enemies.remove(enemy)
                        # adds to score once enemy is removed 
                        data.score1 += 1
                        
                if spell == data.reducioSpell2:
                    enemy.reactToReducioHit()
                    data.spells.remove(spell)
                    if enemy.r < 5:
                        data.enemies.remove(enemy)
                        data.score2 +=1 
                        
                if spell == data.kedavraSpell:
                    data.enemies.remove(enemy)
                    data.spells.remove(spell)
                    data.score1 += 1
                    
                if spell == data.kedavraSpell2:
                    data.enemies.remove(enemy)
                    data.spells.remove(spell)
                    data.score2 += 1
    #print("test")
    # dealing with not falling into platforms 
    for platform in data.platforms:
        if data.player1.posX > platform.x1 and data.player1.posX < platform.x2:
            #print(platform.x1)
            if data.player1.posY + 50 > data.ground1:
                #print("Player 1 fell!")
                # brings them back to the start of the game 
                data.player1.posX, data.player1.posY = platform.x1 - 50, \
                data.ground1 - 20
                data.player1.jumping = False 
                data.lives1 -= 1
                break 
        if data.player2.posX > platform.x1 and data.player2.posX < platform.x2:
            if data.player2.posY + 30 > data.ground2:
                #print("Player 2 fell!")
                data.player2.posX, data.player2.posY = platform.x1 - 50, \
                data.ground1 - 20 
                data.player2.jumping = False
                data.lives2 -= 1 
                break 
    
    # get coins 
    for coin in data.coins:
        if data.player1.collidesWithCoin(coin):
            data.score1 += 1
            data.coins.remove(coin)
            break 
        if data.player2.collidesWithCoin(coin):
            data.score2 += 1 
            data.coins.remove(coin)
            break 
            

        
# read file and write file from 15-112 course notes 
def readFileScore(path):
    with open(path, "rt") as f:
        return f.read()  
          
def writeFileScore(path, contents):
    with open(path, "a") as f:
        f.write(contents)
    
    
def drawBack(canvas, data):
    # draws background for recent scores page 
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "dark blue")
    canvas.create_rectangle(20, 20, data.width - 20, data.height-20, \
    fill = "aquamarine")
    canvas.create_rectangle(40, 40, data.width-40, data.height - 40, \
    fill = "dark blue")
    canvas.create_rectangle(60, 60, data.width - 60, data.height- 60, \
    fill = "aquamarine")
    canvas.create_text(data.width/2, 80, text = "Recent Scores", \
    font = "ComicSansMS 40 bold")
    
def redrawAll1(canvas, data):
    # View 
    if data.player1Dead == False and data.player2Dead == False:
        canvas.create_rectangle(0,0,data.width,data.height,\
        fill="light sky blue")
        # ground
        canvas.create_rectangle(0, data.ground1, data.width, data.height/2, \
        fill = "brown")
        
        canvas.create_rectangle(0, data.ground2, data.width, data.height, \
        fill = "brown")
        for platform in data.platforms:
            # draws platforms 
            platform.draw(canvas, data.scrollX)
        canvas.create_line(0, data.height/2, data.worldWidth, data.height/2, \
        width = 4)
        # draws players 
        data.player1.drawPlayer(canvas)
        data.player2.drawPlayer(canvas)
        drawTrees(canvas, data) # trees 
        # draws coins 
        for coin in data.coins:
            coin.draw(canvas, data.scrollX)
        # draws score 
        drawScore(canvas, data)
        drawLives(canvas, data)
        finishPole(canvas, data, data.scrollX)
        for spell in data.spells:
            # draws spells 
            if spell == data.reducioSpell:
                data.reducioSpell.drawSpell(canvas, color = "blue")
            elif spell == data.kedavraSpell:
                data.kedavraSpell.drawSpell(canvas, color = "lawngreen")
            elif spell == data.reducioSpell2:
                data.reducioSpell2.drawSpell(canvas, color = "blue")
            elif spell == data.kedavraSpell2:
                data.kedavraSpell2.drawSpell(canvas, color = "lawngreen")

        for enemy in data.enemies:
            # draws enemies
            enemy.drawEnemy(canvas)
 
    
    # if all lives lost 
    if data.lives1 <= 0:
        data.player1Dead = True
        data.gameOver = True
        #scoreboard(data)
        
    if data.lives2 <= 0:
        data.player2Dead = True 
        data.gameOver = True
        #scoreboard(data)
        
    # in case user decides to pause  
    if data.paused == True:
        isPaused(canvas, data)
    
    if data.player2Dead == True:
        player1Wins(canvas, data)
        score = str(data.score1)
        name = "Player 1"
        # trying to do recent scores 
        stuff = name + ": " + score + "\n"
        if data.gameOver == True:
            writeFileScore("recent.txt", stuff)
            data.gameOver = False 

    if data.player1Dead == True:
        player2Wins(canvas, data)
        score = str(data.score2)
        name = "Player 2"
        stuff = name + ": " + score + "\n"
        if data.gameOver == True:
            writeFileScore("recent.txt", stuff)
            data.gameOver = False 

        

    # crosses the finish line     
    if data.player1.posX > 2300:
        player1Wins(canvas, data)
        
    if data.player2.posX > 2300:
        player2Wins(canvas, data)
        
    # if data.player1Won == True and data.player2Won == True:
    #     # winner based on score 
    #     if data.score1 > data.score2:
    #         data.player2Dead = True 
    #         
    #     elif data.score2 > data.score1:
    #         data.player1Dead = True 
        
        # else:
        #     data.tie = True     
        
    if data.tie == True:
        # both players win 
        canvas.create_rectangle(0, 0, data.width, data.height, fill = "black")
        canvas.create_image(data.width//2, data.height//2, \
        image = data.congrats)
        

        
# run function from 112 course notes
#################################################################
# use the run function as-is
#################################################################
 
# def run1(width=300, height=300):
#     def redrawAllWrapper(canvas, data):
#         canvas.delete(ALL)
#         canvas.create_rectangle(0, 0, data.width, data.height,
#                                 fill='white', width=0)
#         redrawAll1(canvas, data)
#         canvas.update()
# 
#     def mousePressedWrapper(event, canvas, data):
#         mousePressed1(event, data)
#         redrawAllWrapper(canvas, data)
# 
#     def keyPressedWrapper(event, canvas, data):
#         keyPressed1(event, data)
#         redrawAllWrapper(canvas, data)
# 
#     def timerFiredWrapper(canvas, data):
#         timerFired1(data)
#         redrawAllWrapper(canvas, data)
#         # pause, then call timerFired again
#         canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
#     # Set up data and call init
#     class Struct(object): pass
#     data = Struct()
#     data.width = width
#     data.height = height
#     data.timerDelay = 100 # milliseconds
#     root = Tk()
#     init1(data)
#     # create the root and the canvas
#     canvas = Canvas(root, width=data.width, height=data.height)
#     canvas.configure(bd=0, highlightthickness=0)
#     canvas.pack()
#     # set up events
#     root.bind("<Button-1>", lambda event:
#                             mousePressedWrapper(event, canvas, data))
#     root.bind("<Key>", lambda event:
#                             keyPressedWrapper(event, canvas, data))
#     timerFiredWrapper(canvas, data)
#     # and launch the app
#     root.mainloop()  # blocks until window is closed
#     print("bye!")
# 
# run1(600, 600)