import pygame
import random
import collections

from collections import deque

#define some color
black = (0, 0, 0)
white = (255, 255, 255)
gray = (105, 105, 105)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

#size of the window
display_width = 800
display_height = 600

#size of the actual game
gameplay_width = 580
gameplay_height = 580

#size of the score box
scoreSurfaceWidth = 190
scoreSurfaceHeight = 190

#size of the button sections
messageSurfaceWidth = 190
messageSurfaceHeight = 580

#size of various objects
objectWidth = 10
objectHeight = 10

#delay in game
delay = 100

class fruit(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.left = random.randint(0, gameplay_width / 10 - 1) * 10
        self.top = random.randint(0, gameplay_height / 10 - 1) * 10
        self.object = pygame.Rect(self.left, self.top, objectWidth,
                                  objectHeight)

    def update(self):
        self.left = random.randint(0, gameplay_width / 10 - 1) * 10
        self.top = random.randint(0, gameplay_height / 10 - 1) * 10
        self.object = pygame.Rect(self.left, self.top, objectWidth,
                                  objectHeight)

    def getPos(self):
        return (int(self.left), int(self.top))


class snakeBody(pygame.sprite.Sprite):
    def __init__(self, left, top):
        pygame.sprite.Sprite.__init__(self)
        self.left = left
        self.top = top
        self.object = pygame.Rect(self.left, self.top, objectWidth,
                                  objectHeight)

    def update(self, dir):
        if dir == 'left':
            if (self.left >= 10):
                self.left -= 10
            else:
                self.left = 570
            self.object = pygame.Rect(self.left, self.top, objectWidth,
                                      objectHeight)
        elif dir == 'right':
            if (self.left < 570):
                self.left += 10
            else:
                self.left = 0
            self.object = pygame.Rect(self.left, self.top, objectWidth,
                                      objectHeight)
        elif dir == 'up':
            if (self.top >= 10):
                self.top -= 10
            else:
                self.top = 570
            self.object = pygame.Rect(self.left, self.top, objectWidth,
                                      objectHeight)
        elif dir == 'down':
            if (self.top < 570):
                self.top += 10
            else:
                self.top = 0
            self.object = pygame.Rect(self.left, self.top, objectWidth,
                                      objectHeight)
        elif dir == 'stop':
            self.object = pygame.Rect(self.left, self.top, objectWidth,
                                      objectHeight)

    def getPos(self):
        return (int(self.left), int(self.top))

    def setPos(self, left, top):
        self.left = left
        self.top = top
        self.object = pygame.Rect(self.left, self.top, objectWidth,
                                  objectHeight)


class scoreSection(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.object = self.font.render("Score: " + str(self.score), False,
                                       white)

    def update(self):
        self.score += 10
        self.object = self.font.render("Score: " + str(self.score), False,
                                       white)

    def getScore(self):
        return self.score


#main function is where everything is executed
def main():
    pygame.init()
    pygame.font.init()
    #surface of the game itself

    endGame = False

    pygame.display.set_caption('Snakey Snakey Snaked')
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    actualGameSurface = pygame.Surface((gameplay_width, gameplay_height))
    scoreSurface = pygame.Surface((scoreSurfaceWidth, scoreSurfaceHeight))
    messageSurface = pygame.Surface((messageSurfaceWidth,
                                     messageSurfaceHeight))

    chiLongQuaFace = pygame.image.load("clq.jpg").convert()

    snakeList = deque()  #snake list store all snake body parts
    posList = deque([(17, 17)])  #pos list store all position of body parts

    sH = snakeBody(gameplay_width / 2, gameplay_height / 2)
    snakeList.append(sH)  #append the head first

    f = fruit()
    sC = scoreSection()

    clock = pygame.time.Clock()

    direction = 'stop'

    while not endGame:

        gameDisplay.fill(gray)  #reset everything

        gameDisplay.blit(actualGameSurface, (210, 10))
        gameDisplay.blit(scoreSurface, (10, 10))
        gameDisplay.blit(messageSurface, (10, 210))

        actualGameSurface.fill(black)
        scoreSurface.fill(black)
        messageSurface.fill(black)

        actualGameSurface.blit(chiLongQuaFace, (10, 60))
        pygame.draw.ellipse(actualGameSurface, green, f.object)

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    if direction != 'down':
                        direction = 'up'
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    if direction != 'up':
                        direction = 'down'
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if direction != 'right':
                        direction = 'left'
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    if direction != 'left':
                        direction = 'right'
                if event.key == pygame.K_x or event.key == pygame.K_ESCAPE:
                    endGame = True
                    break

        #delay in game
        pygame.time.wait(delay)

        #this is when the snake moves
        sH.update(direction)

        if (sH.getPos() in posList):  #game over when it eats itself
            endGame = True

        if (sH.getPos() == f.getPos()):
            sC.update()  #update score
            f.update()  #update fruit
            print("fruit is at: " + str(f.getPos()))

        else:

            if (snakeList and posList):

                snakeList.popleft()  #remove the first element when its not fruit
                posList.popleft()

        if (direction != 'stop'):
            snakeList.append(sH)
            posList.append(sH.getPos())

        scoreSurface.blit(sC.object, (0, 0))  #update score text

        for x in range(0, len(snakeList)):
            #print(posList[x])
            snakeList[x].setPos(*posList[x])
            # pygame.draw.circle(gameDisplay, white, snakeList[x].getPos(), objectWidth//2)
            pygame.draw.rect(actualGameSurface, white, snakeList[x].object)

        pygame.display.update()

        clock.tick(60)

    # pygame.quit()

    # quit()


if __name__ == '__main__':
    main()
