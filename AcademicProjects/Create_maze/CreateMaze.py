# File: CreateMaze.py

#README: Question2 and the Extra Credit problem have been merged together. 
#The biggest challenge was to modify the union function that visiblely demonstrated that the children
#of smaller representative were getting attached to the ones with higher representative
#(thereby sharing the same color with the that of the representative of the higher node and its children)
#This code contains a bunch of print statements sprinkled everywhere because it
#helped me to debug the code. I didn't remove them from the final submission

from mazelib import Maze,MazeSquare
from pgl import GWindow
import random

GWINDOW_WIDTH = 1000
GWINDOW_HEIGHT = 1000
MAZE_ROWS = 10
MAZE_COLS = 10
SQUARE_SIZE = 36

g = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT)
D = {}#Maintaining a dictionary to see which nodes have been attached to a particular color

def CreateMaze():

    maze = Maze(MAZE_ROWS, MAZE_COLS, SQUARE_SIZE)

    x = (g.getWidth() - maze.getWidth()) / 2
    y = (g.getHeight() - maze.getHeight()) / 2
    createRandomMaze(maze)
    g.add(maze, x, y)

def createRandomMaze(maze):
     
    for square in maze.getSquares():
        str = randomColor()
        while(str in D.keys()):
            str = randomColor()
        square.setColor(str)

        D[str] = [square]
    
    print(D)

    walls = maze.getWalls()
    random.shuffle(walls)

    def step():
        
        if (len(walls)==0):
            timer.stop()
        if(len(walls)>=1):
            wall = walls.pop()
            sq1,sq2 = wall.getSquares()
            g1 = find(sq1)
            g2 = find(sq2)
            print("Squares are",sq1,sq2,"representatives are",g1,g2)
            
            if g1 == g2:
                    print(g1,g2,"Are Same")
                    wall.setColor("Black")
            else:
                print(g1,g2,"Are not same")
                wall.setColor("White")           
                union(sq1,sq2)
        
    timer = g.setInterval(step,100)
    
def find(node):
    """Returns the representative of the set to which node belongs."""
    # Fill this in
    #if(node):
    if(node.getLink() == None):
        return node

    if node.getLink()!= None:
        node.setLink(find(node.getLink())) 
        return node.getLink()
def union(n1, n2):
    """Combines the sets containing these nodes into a single set."""
    # Fill this in
    link(find(n1),find(n2))

def link(x,y):
    if x._rank > y._rank:
        print("Setting y to x", x._rank,y._rank)
        y.setLink(x)
        ycolor = y.getColor()
        print(y,"Y's color is ", ycolor)
        tmp = x.getColor()
        print(x,"X's color is", tmp)
        print(D[ycolor])
        z = D[ycolor]
        while(len(z)>=1): #As long as the values(nodes) associated with that particular color has elements in it, keep transferring them to the node with higher rank
            for i in z:
                print("Iterating through Y's Colors")

                i.setColor(tmp)
                print("Just setting ",i,"to",tmp)
                D[tmp].append(i)
                D[ycolor].remove(i)
                print(D[tmp])
                print(D[ycolor])
                print(len(z))
        print(D[tmp],D[ycolor])

    else:
        print("Setting x to y", x._rank,y._rank)
        x.setLink(y) 
        xcolor = x.getColor()
        print(x,"X's color is ", xcolor)
        tmp = y.getColor()
        print(y,"Y's color is ", tmp)
        print(D[xcolor])
        z = D[xcolor]
        while(len(z)>=1): #As long as the values(nodes) associated with that particular color has elements in it, keep transferring them to the node with higher rank
            for i in z:
                print("Iterating through X's Colors")
                i.setColor(tmp)
                print("Just setting ",i,"to",tmp)
                D[tmp].append(i)
                D[xcolor].remove(i)
                print(D[tmp],len(D[tmp]))
                print(D[xcolor])
                print(len(z))
        print(D[tmp],D[xcolor])
        if x._rank == y._rank:
            y._rank = y._rank + 1

def randomColor():
    """
    Returns a random opaque color expressed as a string consisting
    of a "#" followed by six random hexadecimal digits.
    """
    str = "#"
    for i in range(6):
        str += random.choice(["0", "1", "2", "3", "4", "5", "6", "7",
                              "8", "9", "A", "B", "C", "D", "E", "F"])
    return str

# Startup code
if __name__ == "__main__":
    CreateMaze()
