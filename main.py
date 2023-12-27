import pygame as game
from copy import copy
from typing import List
import math
import time
import numpy as np
from matplotlib import pyplot as plt
#draw a stairs
#draw a player
#draw a flag at the top
#draw energy bar
#write possible movements

class Step:
    def __init__(self, width: float, height: float, bottom_pos: game.math.Vector2) -> None:
        self.width = width
        self.height = height
        self.bottom_pos = bottom_pos
    def draw(self, screen):
        game.draw.line(screen, game.Color("red"), self.bottom_pos, self.bottom_pos+game.math.Vector2(self.width,0),5)
        game.draw.line(screen, game.Color("red"), self.bottom_pos+game.math.Vector2(self.width,0), self.bottom_pos+game.math.Vector2(self.width,-self.height),5)
        
class Stairs:
    def __init__(self, length: int, start_pos: game.math.Vector2, end_pos: game.math.Vector2) -> None:
        self.length = length
        self.start_pos = copy(start_pos)
        self.end_pos = copy(end_pos)
        self.steps: List[Step]= []
        self.step_width = (self.end_pos[0]-self.start_pos[0])/self.length
        self.step_height = (self.end_pos[1]-self.start_pos[1])/self.length
        temp = copy(self.start_pos)
        for i in range(self.length):
            self.steps.append(Step(self.step_width,-self.step_height,copy(temp)))
            temp += game.math.Vector2((self.step_width,self.step_height))
    def draw(self, screen):
        for step in self.steps:
            step.draw(screen)
            
class Player:
    def __init__(self, width: float, height: float, bottom_pos: game.math.Vector2) -> None:
        self.width = width
        self.height = height
        self.bottom_pos = copy(bottom_pos)
    def draw(self,screen):
        game.draw.rect(screen, game.Color("blue"), [self.bottom_pos[0],self.bottom_pos[1]-self.height,self.width,self.height])
    
class Flag:
    def __init__(self,height: float, bottom_pos: game.math.Vector2) -> None:
        self.height = height
        self.bottom_pos = copy(bottom_pos)
        self.top_pos = bottom_pos+game.math.Vector2((0,-height))
    def draw(self,screen):
        game.draw.line(screen,game.Color("black"),self.bottom_pos,self.top_pos,5)
        game.draw.polygon(screen,game.Color("red"),(self.top_pos,(self.bottom_pos+3*self.top_pos)*(1/4)+(self.height/2,0),(self.bottom_pos+self.top_pos)*(1/2)))
    
class EnergyBar:
    def __init__(self, n: int, square_size: float, bottom_pos: game.math.Vector2) -> None:
        self.n = n
        self.square_size = square_size
        self.bottom_pos = copy(bottom_pos)
        self.top_pos = bottom_pos + game.math.Vector2((0,-square_size))
    def draw(self,screen):
        temp = copy(self.top_pos)
        for _ in range(self.n):
            temp2 = copy(self.top_pos+temp)
            game.draw.rect(screen,game.Color("lightgreen"),(temp2[0],temp2[1],self.square_size,self.square_size))
            temp += game.math.Vector2((6*self.square_size/5),0)

class MovementsBar:
    def __init__(self, size: int, bottom_pos: game.math.Vector2) -> None:
        pass
    def draw(self):
        pass
    
def get_trajectory(start_pos, end_pos):
    x0,y0 = start_pos
    x1,y1 = end_pos
    print(x0,y0,x1,y1)
    a,b,c = np.polyfit([x0,(x0+x1)/2,x1],[y0,y1/2,y1],2)
    def ret(x):
        return a*x**2+b*x+c
    return ret

pos1 = game.math.Vector2((0.,1.))
pos2 = game.math.Vector2((10.,35.))
trajectory = get_trajectory(pos1,pos2)
#plt.plot([x/100 for x in range(1000)],[trajectory(x/100) for x in range(1000)])
#plt.show()

game.init()
screen = game.display.set_mode((500,500))
screen.fill(game.Color("white"))
game.display.flip()

energybar = EnergyBar(3,25.,game.math.Vector2((10,40)))
stairs = Stairs(20,  game.math.Vector2(0,700),game.math.Vector2(700,100))
print(stairs.step_height,stairs.step_width)
player = Player(stairs.step_width*.8,stairs.step_height*(-.8),stairs.steps[0].bottom_pos)

flag = Flag(-stairs.step_height*(1.618),stairs.steps[-1].bottom_pos)
flag.draw(screen)

h=700
w=700

game.init()
screen = game.display.set_mode((w,h))
screen.fill(game.Color("white"))

step_n = 0

while step_n < stairs.length-1:
    event = game.event.poll()
    
    screen.fill(game.Color("white"))
   
    keys = game.key.get_pressed()
    if keys[game.K_1]:
        """step_n+=1
        start_pos = copy(player.bottom_pos)
        end_pos = copy(stairs.steps[step_n].bottom_pos)
        print(start_pos)
        print(end_pos)
        trajectory = get_trajectory(start_pos, end_pos)
        temp_x = start_pos[0]
        clock = game.time.Clock()
        while temp_x < end_pos[0]:
            clock.tick(60)
            temp_x += .1
            player.bottom_pos = game.math.Vector2((temp_x,trajectory(temp_x)))
            player.draw(screen)
        player.bottom_pos = copy(end_pos)
        time.sleep(0.2)"""
        step_n+=1
        player.bottom_pos = copy(stairs.steps[step_n].bottom_pos)
        time.sleep(0.2)
    elif keys[game.K_2] and step_n + 2 < stairs.length-1:
        step_n+=2
        player.bottom_pos = copy(stairs.steps[step_n].bottom_pos)
        time.sleep(0.2)
    elif keys[game.K_5] and energybar.n != 0 and step_n + 5 < stairs.length-1:
        step_n+=5
        player.bottom_pos = copy(stairs.steps[step_n].bottom_pos)
        energybar.n -= 1
        time.sleep(0.2)
    
    flag.draw(screen)
    energybar.draw(screen)
    
    player.draw(screen)
    stairs.draw(screen)
    
    if keys[game.K_o]:
        break
    game.display.flip()
game.quit()

