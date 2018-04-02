import pygame as pg 
import random
import math

#define some color
black = (0, 0, 0)
white = (255, 255, 255)
gray = (105, 105, 105)
darkgray = (55, 55, 55)
red = (255, 0, 0)
darkred = (105, 0, 0)
green = (0, 255, 0)
darkgreen = (0, 105, 0)
blue = (0, 0, 255)
darkblue = (0, 0, 105)

shitcolor = (204, 204, 0)

#width and heigh for window is almost always 800* 600
display_width = 800
display_height = 600

#game display
gamedisplay_width = 600
gamedisplay_height = 600

#score display
scoredisplay_width = 200
scoredisplay_height = 600

class block(pg.sprite.Sprite):
    def __init__(self, left, top):
        pg.sprite.Sprite.__init__(self)
        self.left = left
        self.top = top
        self.image = pg.Surface((20,20))
        self.inside = pg.Surface((18,18))
        self.image.fill(gray)
        self.inside.fill(darkgreen)
        self.image.blit(self.inside, (1,1))
        self.rect = self.image.get_rect(topleft = (self.left, self.top))

    def update(self, dir):
        if dir == 'left':
            self.left -= 20
        elif dir == 'right':           
            self.left += 20
        elif dir == 'up':
            self.top -= 20
        elif dir == 'down':
            self.top += 20
        self.rect = self.image.get_rect(topleft = (self.left, self.top))

    def getPos(self):
        return(self.left,self.top)

class staticBlock(pg.sprite.Sprite):
    def __init__(self, left, top):
        pg.sprite.Sprite.__init__(self)
        self.left = left
        self.top = top
    
    def getPos(self):
        return(self.left,self.top)

class cheese(staticBlock):
    def __init__(self, left, top):
        super(cheese, self).__init__(left, top)
        self.image = pg.image.load("Cheese.png")
        self.image = pg.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect(topleft = (left,top))

class mouse(pg.sprite.Sprite):
    def __init__(self, left, top):
        pg.sprite.Sprite.__init__(self)
        self.left = left
        self.top = top
        self.image = pg.image.load("Mouse.png")
        self.image = pg.transform.scale(self.image, (20, 20))
        # self.rect = self.image.get_rect(topleft = (top,left))
    def update(self, dir):
        if dir == 'left':
            if self.left >= 20:
                self.left -= 20

        elif dir == 'right':
            if self.left < 580:           
                self.left += 20
            
        elif dir == 'up':
            if self.top >= 20:
                self.top -= 20

        elif dir == 'down':
            if self.top < 580:
                self.top += 20
    def getPos(self):
        return(self.left,self.top)



class cat(pg.sprite.Sprite):
    def __init__(self, left, top):
        pg.sprite.Sprite.__init__(self)
        self.left = left
        self.top = top
        self.image = pg.image.load("Cat.png")
        self.image = pg.transform.scale(self.image, (20, 20))
        self.moving = True
        self.rect = self.image.get_rect(topleft = (self.left, self.top))

    def update(self, dir):
        # dir now is a number for easy random
        # 0 = left, 1 = lefttop, 2 = top, 3 = topright, 
        # 4 = right, 5 = rightdown, 6= down, 7 = downleft
        if dir == 0:
            if self.left >= 20:
                self.left -= 20

        elif dir == 1:
            if self.left >= 20 and self.top >= 20:           
                self.left -= 20
                self.top -= 20
            
        elif dir == 2:
            if self.top >= 20:
                self.top -= 20
            
        elif dir == 3:
            if self.left < 580 and self.top >= 20:           
                self.left += 20
                self.top -= 20
            
        elif dir == 4:
            if self.left < 580:           
                self.left += 20
            
        elif dir == 5:
            if self.left < 580 and self.top < 580:           
                self.left += 20
                self.top += 20
            
        elif dir == 6:
            if self.top < 580:
                self.top += 20

        elif dir == 7:
            if self.left >= 20 and self.top < 580:
                self.left -= 20
                self.top += 20
        
        self.rect = self.image.get_rect(topleft = (self.left,self.top))
            
    def getPos(self):
        return(self.left,self.top)
    
    def pause(self):
        self.moving = False

    def move(self):
        self.moving = True

    def isMoving(self):
        return self.moving 
    
    def getDist(self, mousePos):
        mouseLeft = mousePos[0]
        mouseTop = mousePos[1]
        leftDist = math.pow(abs(mouseLeft - self.left), 2)
        topDist = math.pow(abs(mouseTop - self.top), 2)
        dist = math.sqrt(leftDist + topDist)
        return dist

class scoreSection(pg.sprite.Sprite):
    
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.score = 0
        self.font = pg.font.SysFont('Comic Sans MS', 30)
        self.image = self.font.render("Score: " + str(self.score), False, white)

    def update(self):
        self.score += 10
        self.image = self.font.render("Score: " + str(self.score), False, white)

def opp(dir):#return the opposite direction lol
    if dir < 4:
        return (dir + 4)
    else:
        return (dir - 4)

def searchForBlock(posTuple, group):
    for elem in group:
        if elem.getPos() == posTuple:
            return True
    return False

def countPausing(group):# count the number of cats paused in a group of cat
    count = 0
    for elem in group:
        if not elem.isMoving():
            count += 1

    return count

def removeSprite(posTuple, group):
    for elem in group:
        if elem.getPos() == posTuple:
            elem.kill()
            break


def main():
    pg.init()

    
    gameOver = False
    pg.display.set_caption('Rodent Revenge by Anh')
    windowSurface = pg.display.set_mode((display_width, display_height))
    gameSurface = pg.Surface((gamedisplay_width, gamedisplay_height))
    scoreSurface = pg.Surface((scoredisplay_width, scoredisplay_height))

    #store all blocks
    blockGroup = pg.sprite.Group()
    blockPosList = []

    #store all cats
    catGroup = pg.sprite.Group()
    catPosList = []
    numOfCat = 1
    catNo = 0
    
    catUpdateTimer = 200
    catUpdateTick = 0
    #store all chesse
    cheeseGroup = pg.sprite.Group()
    cheesePosList = []

    newMouse = mouse(280, 280)

    score = scoreSection()

    #loop to create square of blocks outside
    blockLeft = 100
    while blockLeft <= 480:
        blockTop = 100
        while blockTop <= 480:
            if not (blockTop == 280 and blockLeft == 280):
                newBlock = block(blockLeft, blockTop)
                blockGroup.add(newBlock)
                blockPosList.append(((blockLeft, blockTop)))
            blockTop += 20
        blockLeft += 20

    #official game loop starts here
    while not gameOver:
        windowSurface.fill(black)
        windowSurface.blit(gameSurface, (0,0))
        windowSurface.blit(scoreSurface, (600,0))
        gameSurface.fill(blue)
        scoreSurface.fill(darkred)

        blockToMove = None   

        #cat failed direction list     
        failedDir = []

        #loop to make different cats
        while catNo < numOfCat and numOfCat <= 5: #5 cats at a time fella
            catLeft = random.randint(0, gamedisplay_width/20) * 20
            catTop = random.randint(0, gamedisplay_height/20) * 20

            while (catLeft, catTop) in blockPosList or (catLeft, catTop) in cheesePosList or (catLeft, catTop) in catPosList or (catLeft, catTop) == newMouse.getPos():
                catTop = random.randint(0, gamedisplay_height/20) * 20 #change one only la
            
            newCat = cat(catLeft, catTop)
            catPosList.append((catLeft, catTop))
            catGroup.add(newCat)
            catNo += 1

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_x:#press x always quit the game
                    gameOver = True
                    break

                #move up
                if event.key == pg.K_UP:
                    #if theres a hole in the column up then push 
                    mouseLeft, mouseTop = newMouse.getPos()
                    while mouseTop >= 0:
                        mouseTop -= 20
                        found = searchForBlock((mouseLeft, mouseTop), blockGroup)
                        if not found:#when not found means it meets something halfway
                            break
                    if (mouseLeft, mouseTop) in catPosList: #you might push the cheese to death
                        found = True

                    if mouseTop >= 0:                        
                        if not found:
                            newMouse.update('up')
                            for blocks in blockGroup:
                                if blocks.getPos() == newMouse.getPos():
                                    blockToMove = blocks
                                    blockPosList.remove(blocks.getPos())
                                    blockToMove.update('up')
                                    break
                            if blockToMove:
                                while blockToMove.getPos() != (mouseLeft, mouseTop):
                                    blockToMove.update('up')
                                blockPosList.append(blockToMove.getPos())

                #move down      
                if event.key == pg.K_DOWN:
                    mouseLeft, mouseTop = newMouse.getPos()
                    while mouseTop <= 580:
                        mouseTop += 20
                        found = searchForBlock((mouseLeft, mouseTop), blockGroup)
                        if not found:
                            break
                    if (mouseLeft, mouseTop) in catPosList:
                        found = True

                    if mouseTop <= 580:
                        if not found:
                            newMouse.update('down')
                            for blocks in blockGroup:
                                if blocks.getPos() == newMouse.getPos():
                                    blockToMove = blocks
                                    blockPosList.remove(blocks.getPos())
                                    blockToMove.update('down')
                                    break
                            if blockToMove:
                                while blockToMove.getPos() != (mouseLeft, mouseTop):
                                    blockToMove.update('down')
                                blockPosList.append(blockToMove.getPos())

                #move left
                if event.key == pg.K_LEFT:
                    mouseLeft, mouseTop = newMouse.getPos()
                    while mouseLeft >= 0:
                        mouseLeft -= 20
                        found = searchForBlock((mouseLeft, mouseTop), blockGroup)
                        if not found:
                            break
                    if (mouseLeft, mouseTop) in catPosList:
                        found = True

                    if mouseLeft >= 0:
                        if not found:
                            newMouse.update('left')
                            for blocks in blockGroup:
                                if blocks.getPos() == newMouse.getPos(): 
                                    blockToMove = blocks
                                    blockPosList.remove(blocks.getPos())
                                    blockToMove.update('left')
                                    break
                            if blockToMove:
                                while blockToMove.getPos() != (mouseLeft, mouseTop):
                                    blockToMove.update('left')
                                blockPosList.append(blockToMove.getPos())

                #move right
                if event.key == pg.K_RIGHT:
                    mouseLeft, mouseTop = newMouse.getPos()
                    while mouseLeft <= 580:
                        mouseLeft += 20
                        found = searchForBlock((mouseLeft, mouseTop), blockGroup)
                        if not found:
                            break
                    if (mouseLeft, mouseTop) in catPosList:
                        found = True

                    if mouseLeft <= 580:
                        if not found:
                            newMouse.update('right')
                            for blocks in blockGroup:
                                if blocks.getPos() == newMouse.getPos(): 
                                    blockToMove = blocks
                                    blockPosList.remove(blocks.getPos())
                                    blockToMove.update('right')
                                    break
                            if blockToMove:
                                while blockToMove.getPos() != (mouseLeft, mouseTop):
                                    blockToMove.update('right')
                                blockPosList.append(blockToMove.getPos())

                #press a to debug all the block position
                if event.key == pg.K_a:

                    print("cat group has: " + str(len(catGroup)))
                    for shit in catPosList:
                        print("them cats at: " + str(shit))
                    
                    for shit in cheesePosList:
                        print("them cheese at: " + str(shit))
        

        if catUpdateTick == catUpdateTimer:
            for cats in catGroup:
                failedDir = []#this is for absolute nono direction
                
                initialPos = cats.getPos()
                if cats.getDist(newMouse.getPos()) <= 60: #if near mouse
                    # print("Danger is near hahaha")
                    wrongDir = []#this is for not desired direction
                    prevDist = cats.getDist(newMouse.getPos())
                    prevPos = cats.getPos()
                    catDir = random.randint(0,7)
                    cats.update(catDir)
                    
                    while len(failedDir) < 9:

                        if cats.getPos() in blockPosList or cats.getPos() == prevPos or cats.getDist(newMouse.getPos()) >= prevDist:
                            if cats.getPos() != prevPos:
                                if cats.getDist(newMouse.getPos()) >= prevDist and cats.getPos() not in blockPosList:
                                    wrongDir.append(catDir)
                                cats.update(opp(catDir))
                            failedDir.append(catDir)
                            catDir += 1
                            catDir %= 8
                            cats.update(catDir)
                        else:
                            break

                    if cats.getPos() in blockPosList or cats.getPos() == prevPos:
                        if cats.getPos() in blockPosList:
                            cats.update(opp(catDir))
                        for dir in wrongDir:
                            cats.update(dir)
                            break

                else:
                    prevPos = initialPos
                    catDir = random.randint(0,7)
                    cats.update(catDir)

                    while cats.getPos() in blockPosList or cats.getPos() == prevPos:
                        failedDir.append(catDir)#append to the list of failure

                        if cats.getPos() in blockPosList:
                            cats.update(opp(catDir))#go back to previous

                        if failedDir.count(catDir) >= 2:
                            # cats.pause()
                            break 

                        prevPos = cats.getPos()
                        catDir += 1
                        catDir %= 8
                        cats.update(catDir)
                    
                catPosList.remove(initialPos)
                catPosList.append(cats.getPos())  

                if cats.getPos() != initialPos:# after cat can accidentally escape, it will move again
                    cats.move()
                else:
                    cats.pause()       

                

            if countPausing(catGroup) ==  len(catGroup):
                for cats in catGroup:
                    newCheese = cheese(cats.getPos()[0],cats.getPos()[1])
                    cheeseGroup.add(newCheese)
                    cheesePosList.append(cats.getPos())
                    cats.kill()
                    catPosList.remove(cats.getPos())

                catNo = 0
                numOfCat += 1

            catUpdateTick = 0
        catUpdateTick += 1

        for cheeseItem in cheeseGroup:
            if cheeseItem.getPos() in blockPosList:
                cheesePosList.remove(cheeseItem.getPos())
                cheeseItem.kill()
                


        if newMouse.getPos() in cheesePosList:
            score.update()
            removeSprite(newMouse.getPos(), cheeseGroup)
            cheesePosList.remove(newMouse.getPos())

        if newMouse.getPos() in catPosList:
            print("CAT IS EATING MOUSE")
            gameOver = True
            

        blockGroup.draw(gameSurface)
        catGroup.draw(gameSurface)
        cheeseGroup.draw(gameSurface)
        
        gameSurface.blit(newMouse.image, newMouse.getPos())
        scoreSurface.blit(score.image, (0,0))#update score text
        pg.display.update()


if __name__ == '__main__':
    main()