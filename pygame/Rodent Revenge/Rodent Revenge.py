import pygame as pg 
import random

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
    
    def stop(self):
        self.moving = False

    def isMoving(self):
        return self.moving


def opp(dir):#return the opposite direction lol
    if dir < 4:
        return (dir + 4)
    else:
        return (dir - 4)

def searchForBlock(leftVal, topVal, group):
    for elem in group:
        if elem.getPos() == (leftVal, topVal):
            return True
    return False

def main():
    pg.init()

    
    gameOver = False
    pg.display.set_caption('Rodent Revenge by Anh')
    windowSurface = pg.display.set_mode((display_width, display_height))
    gameSurface = pg.Surface((gamedisplay_width, gamedisplay_height))

    #store all blocks
    blockGroup = pg.sprite.Group()
    blockPosList = []

    #store all cats
    catGroup = pg.sprite.Group()
    catPosList = []
    numOfCat = 1
    catNo = 0
    
    #store all chesse
    cheeseGroup = pg.sprite.Group()
    cheesePosList = []

    newMouse = mouse(280, 280)

    
    catUpdateTimer = 200
    catUpdateTick = 0

    newCheese = None

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
        gameSurface.fill(blue)

        blockToMove = None   

        #cat failed direction list     
        failedDir = []

        #loop to make different cats
        #change this loop because different blocks are moved 
        #so you cant generate new position using this loop
        while catNo < numOfCat and numOfCat < 4: #4 cats at a time fella
            catLeft = random.randint(0, gamedisplay_width/20) * 20
            if catLeft >= 100 and catLeft <= 500:
                catTop = random.randint(0, 9)
                if catTop < 5:
                    catTop = catTop * 20
                else:
                    catTop = catTop * 20 + 400
            else:
                catTop = random.randint(0, gamedisplay_height/20) * 20

            newCat = cat(catLeft, catTop)
            catPosList.append((catLeft, catTop))
            catGroup.add(newCat)
            catNo += 1
            print("initial Pos is: " + str((catLeft, catTop)))

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
                        found = searchForBlock(mouseLeft, mouseTop, blockGroup)

                        if not found:
                            break

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
                        found = searchForBlock(mouseLeft, mouseTop, blockGroup)

                        if not found:
                            break

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
                        found = searchForBlock(mouseLeft, mouseTop, blockGroup)

                        if not found:
                            break

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
                        found = searchForBlock(mouseLeft, mouseTop, blockGroup)

                        if not found:
                            break

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
                    # for shit in blockPosList:
                    #     print(shit)
                    
                    for shit in cheesePosList:
                        print(shit)
        

        if catUpdateTick == catUpdateTimer:
            for cats in catGroup:
                failedDir = []
                if cats.isMoving():
                
                    initialPos = cats.getPos()
                    prevPos = cats.getPos()
                    catDir = random.randint(0,7)
                    cats.update(catDir)

                    while cats.getPos() in blockPosList or cats.getPos() == prevPos:
                        failedDir.append(catDir)#append to the list of failure

                        if cats.getPos() in blockPosList:
                            cats.update(opp(catDir))#go back to previous

                        if failedDir.count(catDir) >= 2:
                            cats.stop()

                            print("current catdir is: " + str(catDir))
                            for dir in failedDir:
                                print(dir)
                            

                            break 

                        prevPos = cats.getPos()
                        catDir += 1
                        catDir = catDir % 8
                        cats.update(catDir)
                    
                    catPosList.remove(initialPos)
                    catPosList.append(cats.getPos())

                    # print("pos before: " + str(cats.getPos()))
                    # print("pos after: " + str(initialPos))
                    
                else:
                    # print("this cat ain moving")
                    newCheese = cheese(cats.getPos()[0],cats.getPos()[1])
                    cheeseGroup.add(newCheese)
                    cheesePosList.append(cats.getPos())
                    cats.kill()
                    
                    # newCat = None #because now is only 1 cat
                
                if len(catGroup) == 0:
                    catNo = 0
                    numOfCat += 1
                        
            catUpdateTick = 0
        catUpdateTick += 1
            

        blockGroup.draw(gameSurface)
        catGroup.draw(gameSurface)
        cheeseGroup.draw(gameSurface)
        
        gameSurface.blit(newMouse.image, newMouse.getPos())

        pg.display.update()


if __name__ == '__main__':
    main()