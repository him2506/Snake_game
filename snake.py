import pygame
import time
import random
import math
from pygame.locals import *
SIZE = 40 

class Game():
    def __init__(self) -> None:
        # initiate pygame 
        pygame.init()
        pygame.mixer.init()
        self.play_bg_music()
        self.sc = 0
        self.surface = pygame.display.set_mode((800,600)) # Surface vairible is our window.
        self.render_bg()
        self.snake = Snake(self.surface,1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self,x1,y1,x2,y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 +SIZE:
                return True
        return False

    def play_sound(self,sound):
        sound = pygame.mixer.Sound(f"{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def play_bg_music(self):
        pygame.mixer.music.load("bg.mp3")
        pygame.mixer.music.play()
    
    def render_bg(self):
        bg = pygame.image.load('background.jpg')
        self.surface.blit(bg,(0,0))
    
    def play(self):
        self.render_bg()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        # Snake collide with apple
        if self.is_collision(self.snake.block_x[0],self.snake.block_y[0],self.apple.x,self.apple.y):
            self.play_sound("doung")
            self.snake.increase_length()
            self.apple.move()
            self.sc = math.floor(self.sc*1.3) +1 

        # Snake collide with boundary
        self.bg_collide()

        # Snake collide with itself
        for i in range(3,self.snake.length):
            if self.is_collision(self.snake.block_x[0],self.snake.block_y[0],self.snake.block_x[i],self.snake.block_y[i]):
                self.play_sound("crash")
                raise "Collision"

    def bg_collide(self):
        if self.snake.block_x[0] >=800 or self.snake.block_x[0] < 0 :
            self.play_sound("crash")  
            raise
        if self.snake.block_y[0] >=600 or self.snake.block_y[0] < 0 :
            self.play_sound("crash")  
            raise
        
    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score {self.sc}",True,(255,255,255))
        self.surface.blit(score,(700,20))
        
    def show_game_over(self):
        self.render_bg()
        font = pygame.font.SysFont('arial',35)
        line1 = font.render(f"Game Over ! Your Score is {self.sc}",True,(255,255,255))
        self.surface.blit(line1,(200,200))
        line2 = font.render("To play again press Enter. To exit press escape",True,(255,255,255))
        self.surface.blit(line2,(120,250))
        pygame.display.flip()

        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface,1)
        self.apple = Apple(self.surface)
        self.sc = 0


    def run(self):
        running = True
        pause = False
        #self.play_bg_music()
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN: # When event will be pressing any key in keyboard.
                    if event.key == K_ESCAPE: # if keyboard button will be ESC then exit the screen.
                        running = False
                    elif event.key == K_UP:
                        self.snake.move_up()
                    elif event.key == K_DOWN:
                        self.snake.move_down()
                    elif event.key == K_LEFT:
                        self.snake.move_left()
                    elif event.key == K_RIGHT:
                        self.snake.move_right()
                    elif event.key == K_RETURN:
                        pause = False
                        pygame.mixer.music.unpause()
                elif event.type == QUIT:  # When we click on cancle in window.
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            x =  0.2/(self.snake.length*1.1)
            time.sleep(x)



class Snake():
    def __init__(self,parent_screen,length) -> None:
        self.parent_screen = parent_screen
        self.length = length
        self.block = pygame.image.load("block.jpg").convert() # our yellow block
        self.block_x = [SIZE]*self.length
        self.block_y = [SIZE]*self.length
        self.direction = 'down'
        
    def increase_length(self):
        self.length +=1
        self.block_x.append(-1)
        self.block_y.append(-1)   
    def draw(self):
        #self.parent_screen.fill((255,0,255))
        for i in range(self.length):
            self.parent_screen.blit(self.block,(self.block_x[i],self.block_y[i]))
        pygame.display.flip()
    def move_up(self):
        self.direction = 'up'
    def move_down(self):
        self.direction = 'down'
    def move_left(self):
        self.direction = 'left'
    def move_right(self):
        self.direction = 'right'
    def walk(self):
        for i in range(self.length-1,0,-1):
            self.block_x[i] = self.block_x[i-1]
            self.block_y[i] = self.block_y[i-1]

        if self.direction == 'up':
            self.block_y[0] -= SIZE
        if self.direction == 'down':
            self.block_y[0] += SIZE
        if self.direction == 'left':
            self.block_x[0] -= SIZE
        if self.direction == 'right':
            self.block_x[0] += SIZE
        self.draw()
        




class Apple():
    def __init__(self,parent_screen) -> None:
        self.apple = pygame.image.load("apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = random.randint(0,19)*SIZE
        self.y = random.randint(0,14)*SIZE
    def draw(self):
        self.parent_screen.blit(self.apple,(self.x,self.y))
        pygame.display.flip()
    def move(self):
        self.x = random.randint(0,19)*SIZE
        self.y = random.randint(0,14)*SIZE
        self.draw()






if __name__ == "__main__":
    game = Game()
    game.run()














# def draw_back():
#     surface.fill((255,0,255)) # This will clear the screen first then draw the block new position in screen.
#     surface.blit(block,(block_x,block_y))
#     pygame.display.flip()



    # initiate pygame 
    #pygame.init()
    #surface = pygame.display.set_mode((800,500)) # Surface vairible is our window.
    # Filling the surface(window) with manual color
    #surface.fill((255,0,255))

    # block = pygame.image.load("block.jpg").convert() # our yellow block
    # block_x = 100
    # block_y = 100
    #surface.blit(block,(block_x,block_y)) # surface m draw kro. block ko at location (100,100) 

    #pygame.display.flip() # This will update new updates in screen.

    #time.sleep(5) # used for seeing windows.
    # running = True
    # while running:
    #     for event in pygame.event.get():
    #         if event.type == KEYDOWN: # When event will be pressing any key in keyboard.
    #             if event.key == K_ESCAPE: # if keyboard button will be ESC then exit the screen.
    #                 running = False
    #             elif event.key == K_UP:
    #                 block_y = block_y - 10
    #             elif event.key == K_DOWN:
    #                 block_y = block_y +  10
    #             elif event.key == K_LEFT:
    #                 block_x = block_x - 10
    #             elif event.key == K_RIGHT:
    #                 block_x = block_x +  10
    #             draw_back()
                    
    #         elif event.type == QUIT:  # When we click on cancle in window.
    #             running = False


