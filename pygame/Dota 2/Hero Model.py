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

class Hero(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.center = (800 // 2, 600 // 2)
        self.radius = 30
        self.destination = None

    def setDest(self,destination):
        self.destination = destination

    def move(self):
        # self.center
        pass

    


def main():
    pg.init()

    gameOver = False
    pg.display.set_caption('Dota 2 by Anh')
    windowSurface = pg.display.set_mode((display_width, display_height))

    mirana = Hero()

    while not gameOver:
        windowSurface.fill(gray)

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_x:#press x always quit the game
                    gameOver = True

            if event.type == pg.MOUSEBUTTONDOWN:
                
                if event.button == 3:
                    mousePos = pg.mouse.get_pos()
                    # print(mirana.destination, mirana.center)
                    mirana.setDest(mousePos)
                    
                    print(mirana.destination, mirana.center)


        # while(mirana.center != mirana.destination):
            # mirana.move()


        pg.draw.circle(windowSurface, blue, mirana.center, mirana.radius)
        


        pg.display.update()


if __name__ == '__main__':
    main()