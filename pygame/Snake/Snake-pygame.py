import pygame
import random
import collections

from collections import deque

#define some color
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

#tuple
#size of the window
display_width = 800
display_height = 600

#height and width of each module of Snake head is square, body is circle
objectWidth = 10
objectHeight = 10

snakeLength = 1 #to be increment by 1 everytime

#snake is of sprite group because of multiple components
class fruit(pygame.sprite.Sprite):
    
    left = random.randint(0, display_width/10) * 10
    top = random.randint(0, display_height/10) * 10
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.object = pygame.Rect(self.left, self.top, objectWidth, objectHeight)

    def update(self):
        self.left = random.randint(0, display_width/10) * 10
        self.top = random.randint(0, display_height/10) * 10
        self.object = pygame.Rect(self.left, self.top, objectWidth, objectHeight)

    def getPos(self):
        return (self.left, self.top)

class snakeBody(pygame.sprite.Sprite):

    def __init__(self, left, top):
        pygame.sprite.Sprite.__init__(self)
        self.left = left
        self.top = top
        self.object = pygame.Rect(self.left, self.top, objectWidth, objectHeight)

    def update(self,dir):
        if dir == 'left':
            if(self.left >= 10):
                self.left -= 10
            else:
                self.left = 790
            self.object = pygame.Rect(self.left, self.top, objectWidth, objectHeight)
        elif dir == 'right':
            if(self.left < 790):
                self.left += 10
            else:
                self.left = 0
            self.object = pygame.Rect(self.left, self.top, objectWidth, objectHeight)
        elif dir == 'up':
            if(self.top >= 10):
                self.top -= 10
            else:
                self.top = 590
            self.object = pygame.Rect(self.left, self.top, objectWidth, objectHeight)
        elif dir == 'down':
            if(self.top < 590):
                self.top += 10
            else:
                self.top = 0
            self.object = pygame.Rect(self.left, self.top, objectWidth, objectHeight)
        elif dir == 'stop':
            self.object = pygame.Rect(self.left, self.top, objectWidth, objectHeight)
    
    def getPos(self):
        return (self.left, self.top)

    def setPos(self, left, top):
        self.left = left
        self.top = top
        self.object = pygame.Rect(self.left, self.top, objectWidth, objectHeight)

#P p

class scoreSection(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.object = self.font.render("Score: " + str(self.score), False, white)

    def update(self):
        self.score += 10
        self.object = self.font.render("Score: " + str(self.score), False, white)

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

    snakeList = deque()#snake list store all snake body parts
    snakeGroup = pygame.sprite.Group()
    posList = deque([(17,17)]) #pos list store all position of body parts

    prevLeft = display_width/2
    prevTop = display_height/2
    
    sH = snakeBody(prevLeft, prevTop)
    snakeList.append(sH)#append the head first

    f = fruit()
    sC = scoreSection()


    clock = pygame.time.Clock()

    direction = 'stop'

    while not endGame:

        
        
        gameDisplay.fill(black)#reset everything
        
        pygame.draw.ellipse(gameDisplay, white, f.object)
        

        for event in pygame.event.get():
            #if you hit the 'x' on keyboard
            if event.type == pygame.QUIT:
                endGame = True


            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_w:
                    direction = 'up'
                if event.key == pygame.K_s:
                    direction = 'down'
                if event.key == pygame.K_a:
                    direction = 'left'
                if event.key == pygame.K_d:
                    direction = 'right'
                if event.key == pygame.K_x:
                    endGame = True
                    break
            
        pygame.time.wait(50)
        
        #this is when the snake moves
        sH.update(direction)

        
        if(sH.getPos() in posList):#game over when it eats itself
            endGame = True

        if(sH.getPos() == f.getPos()):
            sC.update()#update score
            f.update()#update fruit
            print("fruit is at: " + str(f.getPos())) 
            
        else:

            if(snakeList and posList):
            
                snakeList.popleft()#remove the first element when its not fruit
                posList.popleft()

        if(direction != 'stop'):
            snakeList.append(sH)
            posList.append(sH.getPos())
        
        
        gameDisplay.blit(sC.object, (0,0))#update score text
        
        for x in range(0, len(snakeList)):
            #print(posList[x])
            snakeList[x].setPos(*posList[x])
            pygame.draw.rect(gameDisplay, white, snakeList[x].object)
        

        pygame.display.update()

        clock.tick(60)

    

    

    pygame.quit()

    quit()

if __name__ == '__main__':
    main()
