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


class SpaceShip(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.left = display_width / 2 - 30
        self.top = display_height - 30
        self.image = pg.Surface((60,30))
        self.image.fill(darkblue)
        # self.rect = self.image.get_rect(topleft = (self.left, self.top))
    
    def getPos(self):
        return (self.left, self.top)

    def move(self,left):
        self.left = left
        # self.rect = self.image.get_rect(topleft = (self.left, self.top))

    

class Bullet(pg.sprite.Sprite):
    def __init__(self,left):
        pg.sprite.Sprite.__init__(self)
        self.left = left
        self.top = display_height - 30
        self.object = pg.Rect(self.left, self.top, 6, 16)

    def rise(self):
        self.top -= 6
        self.object = pg.Rect(self.left, self.top, 6, 16)

    def getPos(self):
        return (self.left, self.top)

class Monster(pg.sprite.Sprite):
    def __init__(self,left,top):
        pg.sprite.Sprite.__init__(self)
        self.left = left
        self.top = top
        self.image = pg.Surface((60,30))

    def fillColor(self,color):
        self.image.fill(color)



def main():
    pg.init()

    gameOver = False
    pg.display.set_caption('Space Invader by Anh')
    windowSurface = pg.display.set_mode((display_width, display_height))

    monsterGroup = []

    
    bulletGroup = []
    ship = SpaceShip()

    while not gameOver:
        windowSurface.fill(gray)

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_x:#press x always quit the game
                    gameOver = True

            if event.type == pg.MOUSEBUTTONUP:
                bullet = Bullet(ship.left + 27)
                bulletGroup.append(bullet)

        for bullets in bulletGroup:
            bullets.rise()
            pg.draw.rect(windowSurface, red, bullets.object)

        mousePos = pg.mouse.get_pos()
        if mousePos[0] >= 740:
            ship.move(740)
        else:
            ship.move(mousePos[0])
               
        windowSurface.blit(ship.image, ship.getPos())
        pg.display.update()


if __name__ == '__main__':
    main()