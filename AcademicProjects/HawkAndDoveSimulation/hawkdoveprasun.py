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
        self.birdList = []
#initializing list of all birds in the world
    def update(self):
        currentBirds = []
        for i in self.birdList:
            currentBirds.append(i)
        for b in currentBirds:
            b.update()
#Im running two loops here so that only birds currently in the world will be checked
#and not newly created birds. Originally, new birds were added to the birdList as the program ran and thus
#new birds started out with less then full health

    def free_food(self,x):
        i = 0
        if len(self.birdList) == 0:
            return None
#if there are no birds in the world, return None
        while i <x:
            random.choice(self.birdList).eat()
            i+=1
#randomly gives food to birds in birdList

    def conflict(self,x):
        i = 0
        if len(self.birdList) == 0:
            return None
#if there are no birds in the world, return None
        while i <x:
            random.shuffle(self.birdList)
            self.birdList[0].encounter(self.birdList[1])
            i+=1
#Im shuffling the list and then taking the first two elements in order to pick random birds
#yet keep track of them. This prevents a bird from encountering itself

    """
    def status(self):
        hawkCount = 0
        doveCount = 0
        defensiveCount = 0
        for i in self.birdList:
            if i.species == "Dove":
                doveCount+=1
            elif i.species == "Hawk":
                hawkCount +=1
            else:
                defensiveCount +=1
        if doveCount == 1:
            print("1 Dove")
        if doveCount != 1:
            print(str(doveCount)+ " Doves")
        if hawkCount == 1:
            print("1 Hawk")
        if hawkCount != 1:
            print(str(hawkCount)+ " Hawks")
        if defensiveCount == 1:
            print("1 Defensive")
        if defensiveCount != 1:
            print(str(defensiveCount)+ " Defensives")
    """
#This code is now useless but I wrote it so I assume you want it



    def evolvingPlot(self):
        weight_List = []
        Agression_List = []
        for bird in self.birdList:
            weight_List.append(bird.weight)
            Agression_List.append(bird.agression)
        plot(weight_List,Agression_List)
#checks everybird in birdList and updates the both the weight list and agression list
#in the same run of the loop inorder to correlate weight and agression values of
#the same bird



class Bird:
    """
    def __init__(self,world, weight = None, Defend_choice = None):
        self.health = 100
        self.world = world
        world.birdList.append(self)
        self.vicinity = [self]
        if Defend_choice == None:
            Defend_choice = random.random()
        self.Defend_choice = Defend_choice
        if weight == None:
            weight = random.uniform(1,3)
        self.weight = weight
    """
#Here was the original init function of Bird, I ended up moving the entire init function
#to evolving 
    def eat(self):
        self.health += foodbenefit

    def injured(self):
        self.health -= injurycost

    def display(self):
        self.health -= displaycost

    def die(self):
        self.world.birdList.remove(self)

    def update(self):
        self.health-= (.4 + .6*self.weight)
        if self.health<= 0:
            self.die()
#Evolving.update() calls to here and then proceeds to reproduce new birds
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
#The original encounter method
#This code is useless but again, I wrote it so I assume you want it



class Evolving(Bird):
    def __init__(self,world, weight = None, agression = None):
        self.health = 100
        self.world = world
        world.birdList.append(self)
        self.vicinity = [self]
        if agression == None:
            agression = random.random()
        self.agression = agression
        if weight == None:
            weight = random.uniform(1,3)
        self.weight = weight
#I moved the entire init function here becasue I was having issues when both Bird
#and Evolving had init. I dont know if theres a way to have init functions in both
#Bird and Evolving but this was an easy fix

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
#The new encounter. In order to have the bird win the correct ratio of times, I first
#find the ratio of how often the bird should win against the other bird(w1/(w1 + w2))
# and then test to see if that value is greater then a random value between 0 and 1.
#If it is, the bird will win, if it isnt, the bird will lose. this converts a ratio 
#into a probability of a certain boolean value. I tested it, the ratio of resulting
#True/False 's equaled the ratio that determined how often the bird should win

    def defend_choice(self):
        if self.agression>random.random():
            return True
        else:
            return False
#similar to encounter(), im converting the ratio value into a probability of a certain
#boolean

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

#So this nightmare directs the new baby bird into one of the 16 possible combinations of 
#inherited weight and agression from their parent
#there are 16 combinations because weight and agression could each become one of four
#things (minimum, smaller, larger, maximum). those 4*4 = 16
#yes. i tested each case.





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
#These are all the original Bird creators, I assume you wanted to see them, though
#they are all now useless


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

#A fun experiment to do would be to plot the population size over time. I printed 
#the population size in the above for loop and saw that there is a maximum population 
#that the birds rise to on their first surge before dropping back down to
#a more sustainable population size 


