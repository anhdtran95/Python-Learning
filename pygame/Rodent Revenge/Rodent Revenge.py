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
        self.image.fill(darkgray)
        self.inside.fill(gray)
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
            self.left -= 20

        elif dir == 'right':           
            self.left += 20
            
        elif dir == 'up':
            self.top -= 20

        elif dir == 'down':
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
    pg.display.set_caption('Game by Anh')
    windowSurface = pg.display.set_mode((display_width, display_height))
    gameSurface = pg.Surface((gamedisplay_width, gamedisplay_height))

    blockGroup = pg.sprite.Group()

    newMouse = mouse(280, 280)

    #loop to create square of blocks outside
    blockLeft = 100
    while blockLeft <= 480:
        blockTop = 100
        while blockTop <= 480:
            if not (blockTop == 280 and blockLeft == 280):
                newBlock = block(blockLeft, blockTop)
                blockGroup.add(newBlock)
            blockTop += 20
        blockLeft += 20

    while not gameOver:
        windowSurface.fill(black)

        windowSurface.blit(gameSurface, (0,0))

        gameSurface.fill(green)



        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_x:#press x always quit the game
                    gameOver = True
                    break
                if event.key == pg.K_UP:
                    newMouse.update('up')
                    for blocks in blockGroup:
                        if blocks.getPos()[0] == newMouse.getPos()[0] and blocks.getPos()[1] <= newMouse.getPos()[1]: #directly above mouse
                            # print(blocks.getPos())
                            blocks.update('up')
                            # print(blocks.getPos())
                if event.key == pg.K_DOWN:
                    newMouse.update('down')
                    for blocks in blockGroup:
                        if blocks.getPos()[0] == newMouse.getPos()[0] and blocks.getPos()[1] >= newMouse.getPos()[1]: #directly below mouse
                            blocks.update('down')
                if event.key == pg.K_LEFT:
                    newMouse.update('left')
                    for blocks in blockGroup:
                        if blocks.getPos()[1] == newMouse.getPos()[1]  and blocks.getPos()[0] <= newMouse.getPos()[0]: #to the left of mouse
                            blocks.update('left')
                if event.key == pg.K_RIGHT:
                    newMouse.update('right')
                    for blocks in blockGroup:
                        if blocks.getPos()[1] == newMouse.getPos()[1] and blocks.getPos()[0] >= newMouse.getPos()[0]: #to the right of mouse
                            blocks.update('right')
                if event.key == pg.K_a:
                    for shit in blockGroup:
                        print(shit.getPos())

        

        blockGroup.draw(gameSurface)
        gameSurface.blit(newMouse.image, newMouse.getPos())
        

        pg.display.update()


if __name__ == '__main__':
    main()