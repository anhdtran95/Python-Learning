import pygame as pg 
import random

#define some color
black = (0, 0, 0)
white = (255, 255, 255)
gray = (105, 105, 105)
darkgray = (55, 55, 55)
red = (255, 0, 0)
darkred = (180, 0, 0)
green = (0, 255, 0)
darkgreen = (0, 180, 0)
blue = (0, 0, 255)
darkblue = (0, 0, 180)

colorList = [(red,darkred), (green, darkgreen), (blue, darkblue)]
#size of the window
display_width = 800
display_height = 600

#size of the actual game
gameplay_width = 400
gameplay_height = 600

#size of scoreboard
scoreboard_width = 200
scoreboard_height = 200

#sizef of blocks
block_width = 40
block_height = 40

#blit the inner block at 5 5
innerblock_width = 30
innerblock_height = 30

#bottle surface
bottle_width = 20
bottle_height = 60

#tray surface
tray_width = 100
tray_height = 35

class block(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.width = 40
        self.height = 40
        self.surface = pg.Surface((40,40))

class innerBlock(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.width = 30
        self.height = 30
        self.surface = pg.Surface((30,30))       

        
class scoreSection(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.score = 0
        self.font = pg.font.SysFont('Comic Sans MS', 30)
        self.object = self.font.render("Score: " + str(self.score), False,
                                       black)

    def update(self):
        self.score += 10
        self.object = self.font.render("Score: " + str(self.score), False,
                                       black)

class liveSection(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.live = 3
        self.font = pg.font.SysFont('Comic Sans MS', 30)
        self.object = self.font.render("Lives remaining: " + str(self.live), False,
                                       white)

    def update(self):
        self.live -= 1
        self.object = self.font.render("Lives remaining: " + str(self.live), False,
                                       white)


class bottle(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.top = 0
        self.left = random.randint(4, 34) * 10 #from 40 to 340 because 0 to 400 and 400 - 40 - 20 = 340
        self.object = pg.Rect(self.left, self.top, 20, 60)
    def fall(self):
        self.top += 5
        self.object = pg.Rect(self.left, self.top, 20, 60)
    def getPos(self):
        return (self.left, self.top)

       

def main():
    pg.init()

    gameOver = False

    pg.display.set_caption('Heineken by Anh')
    windowSurface = pg.display.set_mode((display_width, display_height))
    
    gameSurface = pg.Surface((gameplay_width, gameplay_height))
    scoreSurface = pg.Surface((scoreboard_width, scoreboard_height))

    bottleSurface = pg.Surface((bottle_width, bottle_height))
    traySurface = pg.Surface((tray_width, tray_height))

    clock = pg.time.Clock()
    sC = scoreSection()
    lS = liveSection()

    bottleToRemove = bottle() #initialize a random ass bottle
    
    trayLeft = 40
    trayTop = 525
    
    bottleQueue = []
    bottleFail = []
    bottleTimer = 0 #every 10 instance there will be another bottle
    bottleFallRate = 50 #set higher for slower

    score = 0

    while not gameOver:
        windowSurface.fill(black)

        windowSurface.blit(gameSurface, (200,0))
        windowSurface.blit(scoreSurface, (0,0))

        gameSurface.fill(blue)
        scoreSurface.fill(green)

        B = block()
        b = innerBlock()
        

        
        heightToFill = 0
        
        while heightToFill <= gameplay_height:
            if (heightToFill == gameplay_height - 40):
                widthToFill = 0
                while widthToFill <= gameplay_width:
                    gameSurface.blit(B.surface, (gameplay_width - widthToFill, heightToFill))
                    B.surface.fill(darkgray)
                    B.surface.blit(b.surface, (5,5))
                    b.surface.fill(gray)
                    widthToFill += 40
                    
            
            gameSurface.blit(B.surface, (0, gameplay_height - heightToFill))
            B.surface.fill(darkgray)
            B.surface.blit(b.surface, (5,5))
            b.surface.fill(gray)

            gameSurface.blit(B.surface, (360, gameplay_height - heightToFill))
            B.surface.fill(darkgray)
            B.surface.blit(b.surface, (5,5))
            b.surface.fill(gray)

            heightToFill += 40



        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_x or event.key == pg.K_ESCAPE:
                    gameOver = True
                    break  
            
        mousePos = pg.mouse.get_pos()
        if mousePos[0] <= 240:
            trayLeft = 40
        elif mousePos[0] >= 460:
            trayLeft = 260
        else:
            trayLeft = mousePos[0] - 200

        gameSurface.blit(traySurface, (trayLeft, trayTop))

        traySurface.fill(darkred)

        if(bottleTimer == bottleFallRate):
            bottleTimer = 0
            bot = bottle()
            bottleQueue.append(bot)

            
        bottleTimer += 1

        for x in range(0, len(bottleQueue)):
            pg.draw.rect(gameSurface, white, bottleQueue[x].object)
            bottleQueue[x].fall()
            print(bottleQueue[x].getPos())
            if bottleQueue[x].getPos()[1] == trayTop - bottle_height:
                bottleToRemove = bottleQueue[x]
                if (bottleQueue[x].getPos()[0] - tray_width < trayLeft) and (trayLeft < bottleQueue[x].getPos()[0] + bottle_width):
                    sC.update()
                    print(trayLeft)
                    print(bottleQueue[x].getPos()[0] - tray_width)
                    print(bottleQueue[x].getPos()[0] + bottle_width)
                else:
                    lS.update()
                    bottleFail.append(bottleQueue[x])

                if len(bottleFail) == 3:
                    gameOver = True
                    break

        if bottleToRemove in bottleQueue:        
            bottleQueue.remove(bottleToRemove)

        scoreSurface.blit(sC.object, (0,0))#update score text
        windowSurface.blit(lS.object, (0, 200))#update score text
        pg.display.update()

        clock.tick(60)



if __name__ == '__main__':
    main()