###config###

#Amount of Hawks or Doves the model starts off with:
initial_hawks = 1
initial_doves = 1

#Amount of Hawks or Doves the model starts off with:
initial_foods = 150

#Points animals get for food(recomaned between 0-4):
food_nutrition = 2

#Points a given Hawk gets deducted when fighting with other Hawk:
fighting_penalty = 1

#Ratio of food hawks steel from dove:
ratio = 3/4

#Allows animals to store food for the next day:
can_store_food = True

#Food points a animal needs to live:
food_to_live = 1

#Extra food points an animal needs to reproduce:
food_to_reproduce = 2

#Frames per second. The faster this value the faster the simulation.
fps = 10

import tkinter as tk
import random
import time
import numpy as np
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

window_size = 720
root = tk.Tk()
root.maxsize(window_size*2,window_size)
root.minsize(window_size*2,window_size)
root.configure(bg='black')


class Box(tk.Canvas):
    def __init__(self, parent,size ,high = 0, *args, **kwargs):
        tk.Canvas.__init__(self, parent,height= size, width= size, bg= 'black',highlightthickness=high,highlightbackground='green', *args, **kwargs)

box = Box(root,window_size)
box.grid(row=0, column=1)
box2 = Box(root,window_size)
box2.grid(row=0, column=0)

sim_canvas = Box(box,window_size)
sim_canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
matplotlib.use('TkAgg')
plt.style.use('dark_background')
matplotlib.rc('axes',edgecolor='green')
matplotlib.rc('xtick',color='green')
matplotlib.rc('ytick',color='green')
f = Figure(figsize=(window_size/100,window_size/100),dpi=100)
ax = f.add_subplot(111)
class animal:
    def __init__(self,kind:int,intx=0,inty=0,r=window_size/100):
        self.age = 0
        self.kind = kind
        self.pos = (intx,inty)
        self.points = 0
        if self.kind == 1:
            self.sprite = sim_canvas.create_oval(intx - r, inty-r , intx + r , inty + r ,fill="red")
        elif self.kind == 2:
            self.sprite = sim_canvas.create_oval(intx - r, inty-r , intx + r , inty + r ,fill="blue")
    def move(self,x,y):
        sim_canvas.move(self.sprite,x,y)
        self.pos = (x + self.pos[0],y+ self.pos[1])

class food:
    def __init__(self,intx=0,inty=0,nutrition=1,sizemult = window_size*0.003):
        self.animals = list()
        self.nutr = nutrition
        self.size = 2 * sizemult
        self.pos = (intx, inty)
        self.sprite = sim_canvas.create_oval(intx - self.size, inty - self.size, intx + self.size, inty + self.size, fill="green")

class habitat:
    animals = list()
    foods = list()
    selcted = list()
    def __init__(self,size, hawks, doves,foods,food_nutrition = 1):
        self.__class__.size = size
        total = hawks + doves
        steps = (2*np.pi)/total
        shift = size/2
        big = size/2 - size/10
        for i in range(doves):
            intx = big*np.cos(steps*i) + shift
            inty = big*np.sin(steps*i) + shift
            self.__class__.animals.append(animal(2,intx,inty))
        for i in range(hawks):
            intx = big*np.cos(steps*(i+doves)) + shift
            inty = big*np.sin(steps*(i+doves)) + shift
            self.__class__.animals.append(animal(1,intx,inty))
        for i in range(foods):
            a = i * 2.4
            r = ((size/3)*0.33**np.log10(foods)) * np.sqrt(i)
            intx = r*np.cos(a) + shift
            inty = r*np.sin(a) + shift
            self.__class__.foods.append(food(intx,inty,food_nutrition))
    @classmethod
    def go(cls):
        for an in cls.animals:
            dinner = cls.foods[random.randint(0,len(cls.foods))-1]
            dinner.animals.append(an)
            if any(selct is dinner for selct in cls.selcted) == False:
                cls.selcted.append(dinner)
            food_pos = dinner.pos
            an_pos = an.pos
            if food_pos[0] - an_pos[0] != 0:
                m = (food_pos[1] - an_pos[1])/(food_pos[0] - an_pos[0])
                ang = np.arctan(m)
                angpi = ang + np.pi
            else:
                ang = np.pi/2
                angpi = -np.pi/2
            if np.sqrt((20*np.cos(ang) + food_pos[0] - an_pos[0])**2 +(20*np.sin(ang) + food_pos[1] - an_pos[1])**2) < np.sqrt((20*np.cos(angpi) + food_pos[0] - an_pos[0])**2 +(20*np.sin(angpi) + food_pos[1] - an_pos[1])**2):
                x = 20*np.cos(ang) + food_pos[0] - an_pos[0]
                y = 20*np.sin(ang) + food_pos[1] - an_pos[1]
            else:
                x = 20 * np.cos(angpi) + food_pos[0] - an_pos[0]
                y = 20 * np.sin(angpi) + food_pos[1] - an_pos[1]
            del an_pos
            an.move(x,y)
    @classmethod
    def eat(cls,pen=1,ratio=0.66,can_store_food = True):
        for food in cls.selcted:
            if food.animals:
                sim_canvas.itemconfigure(food.sprite,state='hidden')
                conter = Counter([an.kind == 1 for an in food.animals])
                num_hawk = conter[True]
                num_dove = conter[False]
                dove_food = food.nutr * (1 - ratio)
                hawkfood = food.nutr * ratio
                if num_hawk > 1 and num_dove >=1:
                    for an in food.animals:
                        if an.kind == 2:
                            if can_store_food == True:
                                an.points += dove_food/num_dove
                            else:
                                an.points = dove_food/num_dove
                        else:
                            if can_store_food == True:
                                an.points += hawkfood / num_hawk - pen
                            else:
                                an.points = hawkfood / num_hawk - pen
                elif num_hawk == 1 and num_dove >=1:
                    dove_food = food.nutr * (1 - ratio)
                    hawkfood = food.nutr * ratio
                    for an in food.animals:
                        if an.kind == 2:
                            if can_store_food == True:
                                an.points += dove_food/num_dove
                            else:
                                an.points = dove_food/num_dove
                        else:
                            if can_store_food == True:
                                an.points += hawkfood / num_hawk
                            else:
                                an.points = hawkfood / num_hawk
                elif num_hawk > 1 and num_dove == 0:
                    for an in food.animals:
                        if can_store_food == True:
                            an.points += food.nutr / num_hawk - pen
                        else:
                            an.points = food.nutr / num_hawk - pen
                elif num_hawk == 1 and num_dove == 0:
                    for an in food.animals:
                        if can_store_food == True:
                            an.points += food.nutr / num_hawk
                        else:
                            an.points = food.nutr / num_hawk
                elif num_hawk == 0 and num_dove >= 1:
                    for an in food.animals:
                        if can_store_food == True:
                            an.points += food.nutr / num_dove
                        else:
                            an.points = food.nutr / num_dove
                food.animals = list()
        cls.selcted = list()
    @classmethod
    def kill(cls,die = 1,reproduce = 2):
        killed = list()
        cls.newhawks = 0
        cls.newdoves = 0
        for an in cls.animals:
            if an.points < die:
                sim_canvas.delete(an.sprite)
                killed.append(an)
            elif an.points >= reproduce + die:
                an.points -= die
                reprate = np.floor(an.points/reproduce)
                for i in range(int(reprate)):
                    an.points -= reproduce
                    if an.kind == 1:
                        cls.newhawks += 1
                    elif an.kind == 2:
                        cls.newdoves += 1
            else:
                an.points -= die
        for an in killed:
            cls.animals.remove(an)
    @classmethod
    def newday(cls):
        for i in range(cls.newhawks):
            cls.animals.append(animal(1))
        for i in range(cls.newdoves):
            cls.animals.append(animal(2))
        total = len(cls.animals)
        if total != 0:
            steps = (2 * np.pi) / total
        else:
            steps = 0
        shift = cls.size / 2
        big = cls.size / 2 - cls.size / 10
        n = 0
        for an in cls.animals:
            an_pos = an.pos
            x = big * np.cos(steps * n) + shift - an_pos[0]
            y = big * np.sin(steps * n) + shift - an_pos[1]
            an.move(x,y)
            n+=1
        for food in cls.foods:
            sim_canvas.itemconfigure(food.sprite, state='normal')
    @classmethod
    def popdist(cls):
        conter = Counter([an.kind == 1 for an in cls.animals])
        return((conter[True],conter[False]))



def startgame(window_size,initial_hawks,initial_doves,initial_foods,food_nutrition,fighting_penalty,food_to_live,food_to_reproduce,fps,ratio,can_store_food):
    habitat(window_size, initial_hawks, initial_doves, initial_foods, food_nutrition)
    x = range(0, 2)
    y1 =[0, initial_hawks]
    y2=[0, initial_doves]
    y = [y1, y2]
    ax.stackplot(x, y, labels=['Hawks', 'Doves'], colors=['Red', 'Blue'])
    #ax.legend(loc='upper left')
    chart_type = FigureCanvasTkAgg(f, box2)
    chart_type.get_tk_widget().place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    chart_type.draw()
    root.update()
    day = 1

    #while True:
    for i in range(1800):
        time.sleep(fps)

        habitat.go()

        root.update()

        time.sleep(fps)

        habitat.eat(fighting_penalty,ratio,can_store_food)

        root.update()

        time.sleep(fps)

        habitat.kill(food_to_live,food_to_reproduce)

        root.update()

        time.sleep(fps)

        habitat.newday()

        newvals=habitat.popdist()
        ax.clear()

        x = range(0, 2 + day)
        y1.append(newvals[0])
        y2.append(newvals[1])
        y = [y1, y2]
        ax.stackplot(x, y, labels=['Hawks', 'Doves'], colors=['Red', 'Blue'])
        ax.legend(loc='upper left',edgecolor='green')
        chart_type.draw()
        root.update()
        day += 1


startgame(window_size, initial_hawks, initial_doves, initial_foods, food_nutrition, fighting_penalty, food_to_live,food_to_reproduce, 1/fps, ratio, can_store_food)
