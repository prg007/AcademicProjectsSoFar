import random
import tkinter
random.seed()

def plot(xvals, yvals):
    # This is a function for creating a simple scatter plot.  You will use it,
    # but you can ignore the internal workings.
    root = tkinter.Tk()
    c = tkinter.Canvas(root, width=700, height=400, bg='white') #was 350 x 280
    c.grid()
    #create x-axis
    c.create_line(50,350,650,350, width=3)
    for i in range(5):
        x = 50 + (i * 150)
        c.create_text(x,355,anchor='n', text='%s'% (.5*(i+2) ) )
    #y-axis
    c.create_line(50,350,50,50, width=3)
    for i in range(5):
        y = 350 - (i * 75)
        c.create_text(45,y, anchor='e', text='%s'% (.25*i))
    #plot the points
    for i in range(len(xvals)):
        x, y = xvals[i], yvals[i]
        xpixel = int(50 + 300*(x-1))
        ypixel = int(350 - 300*y)
        c.create_oval(xpixel-3,ypixel-3,xpixel+3,ypixel+3, width=1, fill='red')
    root.mainloop()

#Constants: setting these values controls the parameters of your experiment.
injurycost = 10 #Cost of losing a fight  
displaycost = 1 #Cost of displaying between two passive birds  
foodbenefit = 8 #Value of the food being fought over   
init_hawk = 0
init_dove = 0
init_defensive = 0
init_evolving = 150

########
# Your code here
########

class World:

    def __init__(self):
        self.bList = []    #Initializing the list of every bird in the world

    def update(self):
        CBirds = []
        for elm in self.bList:
            CBirds.append(elm)    
        
        for elm in CBirds:
            elm.update()



    def free_food(self,x):
        elm = 0
        if len(self.bList) == 0:
            return None#Returns None if there are no birds in the world

        while elm <x:
            random.choice(self.bList).eat()
            elm+=1


    def conflict(self,x):
        elm = 0
        if len(self.bList) == 0:
            return None#Returns None if there are no birds in the world

        while elm <x:
            random.shuffle(self.bList)
            self.bList[0].encounter(self.bList[1])
            elm+=1
    #Over here the list is randomized and the first two elements are taken to encounter

    """
    def status(self):
        DoveBirdCount = 0
        HawkBirdCount = 0
        DfnsivCnt = 0
        for elm in self.bList:
            if elm.species == "Dove":
                DoveBirdCount+=1
            elif elm.species == "Hawk":
                HawkBirdCount +=1
            else:
                DfnsivCnt +=1
        if DoveBirdCount == 1:
            print("Only 1 Dove Remains")
        if DoveBirdCount != 1:
            print(str(DoveBirdCount)+ " DoveBirds")
        if HawkBirdCount == 1:
            print("Only 1 Hawk Remains")
        if HawkBirdCount != 1:
            print(str(HawkBirdCount)+ " HawkBirds")
        if DfnsivCnt == 1:
            print("1 Defensive")
        if DfnsivCnt != 1:
            print(str(DfnsivCnt)+ " DefensiveBirds")
    """
#Placed within quotes to prevent execution



    def evolvingPlot(self):
        Weight_List = []
        Agression_List = []
        for bird in self.bList:
            Weight_List.append(bird.weight)
            Agression_List.append(bird.agression)
        plot(Weight_List,Agression_List)
    #It first checks for every bird in bList and then updates both the weight list and agression list of that particular bird




class Bird:
    """
    def __init__(self,world, weight = None, Defend_choice = None):
        self.health = 100
        self.world = world
        world.bList.append(self)
        self.vicinity = [self]
        if Defend_choice == None:
            Defend_choice = random.random()
        self.Defend_choice = Defend_choice
        if weight == None:
            weight = random.uniform(1,3)
        self.weight = weight
    """
    #Placed in quotes to prevent execution

    def eat(self):
        self.health += foodbenefit

    def injured(self):
        self.health -= injurycost

    def display(self):
        self.health -= displaycost

    def die(self):
        self.world.bList.remove(self)

    def update(self):
        self.health-= (.4 + .6*self.weight)
        if self.health<= 0:
            self.die()

    """
    def encounter(self,bird):
        self.vicinity.append(bird)
        if self.species == "Dove" or self.species == "Defensive":
            if bird.defend_choice() == False:
                for i in self.vicinity:
                    i.display()
                random.choice(self.vicinity).eat()
            else:
                bird.eat()
        elif self.defend_choice() and self.species == "Hawk" and not bird.defend_choice():
            self.eat()
        else:
            random.shuffle(self.vicinity)
            self.vicinity[0].eat()
            self.vicinity[1].injured()
        self.vicinity.remove(bird)
        """
#Placed in quotes to prevent execution


class Evolving(Bird):
    def __init__(self,world, weight = None, agression = None):
        self.health = 100
        self.world = world
        world.bList.append(self)
        self.vicinity = [self]
        if agression == None:
            agression = random.random()
        self.agression = agression
        if weight == None:
            weight = random.uniform(1,3)
        self.weight = weight


    def encounter(self,bird):
        self.vicinity.append(bird)

        if self.defend_choice() and bird.defend_choice():
            if self.weight/(self.weight+bird.weight)<random.random():
                bird.eat()
                self.injured()
            if self.weight/(self.weight+bird.weight)>random.random():
                self.eat()
                bird.injured()
        elif self.defend_choice() and not bird.defend_choice():
            self.eat()
        elif not self.defend_choice() and bird.defend_choice():
            bird.eat()
        else:
            bird.display()
            self.display()
            random.choice(self.vicinity).eat()
            self.vicinity.remove(bird)

#A ratio was calculated (w1/(w1+w2)) to see how often a bird wins 
#against another bird and then compared against a random value in 
#between 0 and 1. If its greater than the random value the bird wins
#or else the bird loses"""


    def defend_choice(self):
        if self.agression>random.random():
            return True
        else:
            return False
#The ratio value is converted to a boolean probability


    def update(self):
        Bird.update(self)
        if self.health >= 200:
            self.health -=100
            Weight_Mutation = bool(random.getrandbits(1))
            Agression_Mutation = bool(random.getrandbits(1))
            if Weight_Mutation:
                if Agression_Mutation:
                    if self.weight+ .1>= 3:
                        if self.agression + .05 >= 1:
                            newEvolving = Evolving(self.world, 3, 1)
                        else:
                            newEvolving = Evolving(self.world, 3, self.agression+.05)
                    else:
                        if self.agression + .05 >= 1:
                            newEvolving = Evolving(self.world, self.weight+.1, 1)
                        else:
                            newEvolving = Evolving(self.world, self.weight+.1,self.agression+.05)
                else:
                    if self.weight+ .1>= 3:
                        if self.agression - .05 <= 0:
                            newEvolving = Evolving(self.world, 3, 0)
                        else:
                            newEvolving = Evolving(self.world, 3, self.agression-.05)
                    else:
                        if self.agression - .05 <= 0:
                            newEvolving = Evolving(self.world, self.weight+.1, 0)
                        else:
                            newEvolving = Evolving(self.world, self.weight+.1,self.agression-.05)
            else:
                if Agression_Mutation:
                    if self.weight- .1<= 1:
                        if self.agression + .05 >= 1:
                            newEvolving = Evolving(self.world, 1, 1)
                        else:
                            newEvolving = Evolving(self.world, 1, self.agression+.05)
                    else:
                        if self.agression + .05 >= 1:
                            newEvolving = Evolving(self.world, self.weight-.1, 1)
                        else:
                            newEvolving = Evolving(self.world, self.weight-.1,self.agression+.05)
                else:
                    if self.weight- .1<= 1:
                        if self.agression - .05 <= 0:
                            newEvolving = Evolving(self.world, 1, 0)
                        else:
                            newEvolving = Evolving(self.world, 1, self.agression-.05)
                    else:
                        if self.agression - .05 <= 0:
                            newEvolving = Evolving(self.world, self.weight-.1, 0)
                        else:
                            newEvolving = Evolving(self.world, self.weight-.1,self.agression-.05)
#fml

"""The new baby is subjected to many different combinations of weight and aggression 
from their parents"""



"""
class Dove(Bird):
    species = "Dove"

    def update(self):
        Bird.update(self)
        if self.health >= 200:
            self.health -=100
            newDove = Dove(self.world)

    def defend_choice(self):
        return False



class Hawk(Bird):
    species = "Hawk"

    def update(self):
        Bird.update(self)
        if self.health >= 200:
            self.health -=100
            newHawk = Hawk(self.world)

    def defend_choice(self):
        return True


class Defensive(Bird):
    species = "Defensive"

    def update(self):
        Bird.update(self)
        if self.health >= 200:
            self.health -=100
            newDefensive = Defensive(self.world)

    def defend_choice(self):
        return True
"""
#Placed in quotes to prevent execution


########
# The code below actually runs the simulation.  You shouldn't have to do anything to it.
########
w = World()
for i in range(init_dove):
    Dove(w)
for i in range(init_hawk):
    Hawk(w)
for i in range(init_defensive):
    Defensive(w)
for i in range(init_evolving):
    Evolving(w)

for t in range(10000):
    w.free_food(10)  #change to 10
    w.conflict(50)  #change to 50
    w.update()
w.evolvingPlot()  #This line adds a plot of evolving birds. Uncomment it when needed.




