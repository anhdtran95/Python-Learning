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
        self.inside.fill(shitcolor)
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
        self.image = pg.image.load("Cat.png").convert()
        self.image = pg.transform.scale(self.image, (20, 20))
        # self.rect = self.image.get_rect(topleft = (top,left))
    def update(self, dir):
        if dir == 'left':
            self.left -= 20

        elif dir == 'right':           
            self.left += 20
            
        elif dir == 'up':
            self.top -= 20

        elif dir == 'down':
            self.top += 20
            
    def getPos(self):
        return(self.left,self.top)



def main():
    pg.init()

    
    gameOver = False
    pg.display.set_caption('Rodent Revenge by Anh')
    windowSurface = pg.display.set_mode((display_width, display_height))
    gameSurface = pg.Surface((gamedisplay_width, gamedisplay_height))

    blockGroup = pg.sprite.Group()
    blockPosList = []
    directionLockList = []
    # look something like ( left coordinate and down: (240, down) means at 240 from left u cant go down
    # or (left, 220) means at 220 from top u cant go left

    newMouse = mouse(280, 280)

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

    while not gameOver:
        windowSurface.fill(black)

        windowSurface.blit(gameSurface, (0,0))

        gameSurface.fill(darkred)


        blockToMove = None        


        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_x:#press x always quit the game
                    gameOver = True
                    break
                if event.key == pg.K_UP:
                    newMouse.update('up')
                    for blocks in blockGroup:
                        if blocks.getPos() == newMouse.getPos(): #directly above mouse
                            if (blocks.getPos()[0], 'up') not in directionLockList:
                                blockToMove = blocks
                                blockPosList.remove(blocks.getPos())
                                blockToMove.update('up')
                                break
                            else:
                                newMouse.update('down')

                    if blockToMove:
                        while blockToMove.getPos() in blockPosList:
                        
                            #print(blockToMove.getPos())
                            blockToMove.update('up')
                    
                        blockPosList.append(blockToMove.getPos())
                        if blockToMove.getPos()[1] == 0:
                            directionLockList.append((blockToMove.getPos()[0], 'up')) 

                        
                if event.key == pg.K_DOWN:
                    newMouse.update('down')
                    for blocks in blockGroup:
                        if blocks.getPos() == newMouse.getPos(): #directly above mouse
                            if (blocks.getPos()[0], 'down') not in directionLockList:
                                blockToMove = blocks
                                blockPosList.remove(blocks.getPos())
                                blockToMove.update('down')
                                break
                            else:
                                newMouse.update('up')

                    if blockToMove:
                        while blockToMove.getPos() in blockPosList:
                        
                            #print(blockToMove.getPos())
                            blockToMove.update('down')
                    
                        blockPosList.append(blockToMove.getPos())
                        if blockToMove.getPos()[1] == 580:
                            directionLockList.append((blockToMove.getPos()[0], 'down')) 

                if event.key == pg.K_LEFT:
                    newMouse.update('left')
                    for blocks in blockGroup:
                        if blocks.getPos() == newMouse.getPos(): #directly above mouse
                            if ('left', blocks.getPos()[1]) not in directionLockList:
                                blockToMove = blocks
                                blockPosList.remove(blocks.getPos())
                                blockToMove.update('left')
                                break
                            else:
                                newMouse.update('right')

                    if blockToMove:
                        while blockToMove.getPos() in blockPosList:
                        
                            #print(blockToMove.getPos())
                            blockToMove.update('left')
                    
                        blockPosList.append(blockToMove.getPos())
                        if blockToMove.getPos()[0] == 0:
                            directionLockList.append(('left', blocks.getPos()[1])) 

                if event.key == pg.K_RIGHT:
                    newMouse.update('right')
                    for blocks in blockGroup:
                        if blocks.getPos() == newMouse.getPos(): #directly above mouse
                            if ('right', blocks.getPos()[1]) not in directionLockList:
                                blockToMove = blocks
                                blockPosList.remove(blocks.getPos())
                                blockToMove.update('right')
                                break
                            else:
                                newMouse.update('left')

                    if blockToMove:
                        while blockToMove.getPos() in blockPosList:
                        
                            #print(blockToMove.getPos())
                            blockToMove.update('right')
                    
                        blockPosList.append(blockToMove.getPos())
                        if blockToMove.getPos()[0] == 580:
                            directionLockList.append(('right', blocks.getPos()[1])) 
                if event.key == pg.K_a:
                    for shit in blockGroup:
                        print(shit.getPos())

        

        blockGroup.draw(gameSurface)
        gameSurface.blit(newMouse.image, newMouse.getPos())
        

        pg.display.update()


if __name__ == '__main__':
    main()