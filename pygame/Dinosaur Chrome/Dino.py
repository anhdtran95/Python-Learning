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

#earth surface
earth_width = 800
earth_height = 230

class Dino(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.left = 100
        self.top = 300
        self.image = pg.image.load("Dino.png")
        self.state = 'standing' # true for standing up false for ducking down
        self.image = pg.transform.scale(self.image, (50, 70))
        # self.rect = self.image.get_rect(topleft = (self.left, self.top))

    def getPos(self):
        return (self.left, self.top)
    
    def duck(self):
        self.state = 'ducking'
        self.image = pg.image.load("Dino.png")
        self.top = 320
        self.image = pg.transform.scale(self.image, (50, 50))

    def stand(self):
        self.state = 'standing'
        self.image = pg.image.load("Dino.png")
        self.top = 300
        self.image = pg.transform.scale(self.image, (50, 70))

    def fly(self):
        self.state = 'flying'
        self.image = pg.image.load("Dino.png")
        self.top = 280
        self.image = pg.transform.scale(self.image, (50, 70))

    def isStanding(self):
        return (self.state == 'standing')

    def isDucking(self):
        return (self.state == 'ducking')

    def isFlying(self):
        return (self.state == 'flying')




def main():
    pg.init()

    gameOver = False
    pg.display.set_caption('Dino by Anh')
    windowSurface = pg.display.set_mode((display_width, display_height))
    earthSurface = pg.Surface((earth_width, earth_height))
    

    dino = Dino()
    while not gameOver:
        windowSurface.fill(gray)

        windowSurface.blit(earthSurface, (0, 360))

        earthSurface.fill(red)

        for event in pg.event.get():
            if dino.isFlying():
                dino.stand()
                break

            if dino.isDucking():
                dino.stand()
                break

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_x:#press x always quit the game
                    gameOver = True
                if event.key == pg.K_DOWN:#press x always quit the game
                    if dino.isStanding():
                        dino.duck()
                if event.key == pg.K_UP:#press x always quit the game
                    if dino.isStanding():
                        dino.fly()
                


        windowSurface.blit(dino.image,dino.getPos())
        pg.display.update()


if __name__ == '__main__':
    main()