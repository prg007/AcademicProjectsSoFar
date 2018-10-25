"""The code below creates the main class. It displays 
the window title and draws up the canvas for the game. The function
tk.wm_attributes is used to bring up the current window on 
top of all other windows. The function tk.resizable is used to fix
the current window . The parameters 0,0 indicate that the height
and width be fixed for the current window. The canvas.pack() function
is used to restructure the size of the canvas . The update method is
used to bring the application upto date. The PhotoImage function is
used to load an image on the canvas. I have taught myself some of Tkinter 
functions from the following websites : 
1)https://www.tutorialspoint.com/python/tk_pack.htm 
2)https://docs.python.org/3/library/tk.html
3)http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/index.html"""
from tkinter import *
import random
import time

class GMain:
    def __init__(self):
        self.tk = Tk()
        self.tk.title("Help Mario Emerge Reach The Window")#Displays the title at the top of the window 

        
        self.cnvs_height = 500
        self.cnvs_width = 500
        self.bground_color = PhotoImage(file="bground.gif")#The PhotoImage class is used to display images in tkinter
        self.bground_color2 = PhotoImage(file = "bground2.gif")
        self.tk.resizable(0, 0)#This helps to keep the window fixed so that it can't be changed
        
        height = self.bground_color.height()

        self.cnvs = Canvas(self.tk, width=500, height = 500, highlightthickness=0)
        self.cnvs.pack()
        self.tk.update()
        draw_bg = 0
        width = self.bground_color.width()
        for i in range(0, 5):#The total area is 500*500 pixels that's
            for j in range(0, 5):#why we need each loop to run upto 5 times
                if draw_bg == 1:#The following code overlaps 2 background colors and creates a checkered style background color
                    self.cnvs.create_image(i * width, j * height, image=self.bground_color, anchor='nw')
                    draw_bg = 0
                else:
                    self.cnvs.create_image(i * width, j * height, image=self.bground_color2, anchor='nw')
                    draw_bg = 1
        self.lists = []
        self.game_over = None
        self.cnvs.create_text(275,23,anchor = 'c', font = ("Purisa", 10) ,fill = 'orange',text = "SPACE -> JUMP, LEFT ARROW ->  MOVE LEFT, RIGHT ARROW -> MOVE RIGHT")
        self.cnvs.create_text(275,33,anchor = 'c', font = ("Purisa", 10) ,fill = 'orange',text = "If you fall through more than 60 pixels you die!!")
        self.run = True
        self.run2 = True
        self.game_over_display = self.cnvs.create_text(250,250,text = "HURRAY!",state = 'hidden')

    
    def looping(self):                  #For the code below, the loop keeps getting executed until the
                                        #window is closed. The function move is called for every element in
                                        #lists        
        while 1: 
            if self.run == True:
                for x in self.lists:
                    x.movement()
            else:
                #If Mario, reaches the end of window the game over text is displayed by changing its state to Normal
                self.cnvs.create_text(250,250,text = "HURRAY!",fill = 'orange',font = ("Purisa",60))

            if self.run2 == False:#This code takes part of the situation when Mario falls through a distance greater than 60m . The game terminates when this happens
                self.tk.update_idletasks()
                self.tk.update()
                time.sleep(5)#Waits for 5 seconds and then terminates the game
                sys.exit()
            self.tk.update_idletasks()#The tkinder object is updated
            self.tk.update()#and drawn on the screen
            time.sleep(0.02)#Sleeps for a fraction of asecond
                            #before the next iterationn

class Coordinates:#This class describes the position of objects
    def __init__(self,x1=0,y1=0,x2=0,y2=0):#on the game screen
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

def collision_x(set1,set2):#Checks whether 2 objects collide with each other in the horizontal direction
    if set1.x1 > set2.x2 and set1.x1 < set2.x2:
        return True
    elif set1.x2 > set2.x1 and set1.x2 < set2.x2:
        return True
    elif set2.x1 > set1.x1 and set2.x1 < set1.x2:
        return True
    elif set2.x2 > set1.x1 and set2.x2 < set1.x1:
        return True
    else:
        return False

def collision_y(set1, set2):#Checks whether 2 objects collide with each other in the vertical direction
    if (set1.y1 > set2.y1 and set1.y1 < set2.y2) \
            or (set1.y2 > set2.y1 and set1.y2 < set2.y2) \
            or (set2.y1 > set1.y1 and set2.y1 < set1.y2) \
            or (set2.y2 > set1.y1 and set2.y2 < set1.y1):
        return True
    else:
        return False

def left_collison(set1, set2):#This function checks whether left hand side 
    if collision_y(set1, set2):#of one object has hit another object
        if set1.x1 <= set2.x2 and set1.x1 >= set2.x1:
            return True
    return False

def right_collison(co1, co2):#Similar to the previous one, this function checks
    if collision_y(co1, co2):#whether the right hand side of one object has hit another object
        if co1.x2 >= co2.x1 and co1.x2 <= co2.x2:
            return True
    return False

def top_collision(set1, set2):#The top_collison and bottom_collison functions are
    if collision_x(set1, set2):#responsible for checking whether the coordinates have crossed horizontally
        if set1.y1 <= set2.y2 and set1.y1 >= set2.y1:#as opposed to vertically for the previous 2 functions
             return True
    return False

def bottom_collision(y, set1, set2):#The purpose of the additional parameter y is to see
    if collision_x(set1, set2):#whether the newly calculated value is between y1 and y2 values
        y_total = set1.y2 + y
        if y_total >= set2.y1 and y_total <= set2.y2:#as Mario could fall off the landing stations
            return True
    return False

class Lists: #The class Lists provdes two functions to see whether the object has moved
    def __init__(self,game):#and if it returns the objects current position on the screen
        self.game = game
        self.gameover = False
        self.coordinates = None

    def movement(self):#It does nothing over here,so pass is used
        pass

    def coords(self):
        return self.coordinates#Returns the object's co-ordinates at the current position

class LandingPos(Lists):#Responsible for adding the landing objects
    def __init__(self,game,pic,x,y,w,h):
        Lists.__init__(self,game)
        self.pic = pic
        self.image = game.cnvs.create_image(x,y,image = self.pic,anchor = 'nw')#The image which was imported is now drawn on the screen 
        self.coordinates = Coordinates(x,y,x+w,y+h)#w and h are width and height respectively. The coordinates variable which was None has now been overwritten
    

class MovingLandingPos(LandingPos):
    def __init__(self, game, pic, x, y, w, h):
        LandingPos.__init__(self, game, pic, x, y, w, h)
        self.x = 1.5 #The Landing Pos Object moves with this speed
        self.cntr = 0#The Counter is used to change direction
        self.lt = time.time()#We record the time so that the landingpos object does not move too quickly
        self.w = w
        self.h = h

    def coords(self):#Gets Landing Object's position in the game board
        ab = (self.game.cnvs.coords(self.image))#returns the x and y positions of the current image
        self.coordinates.x1 = ab[0]
        self.coordinates.y1 = ab[1]
        self.coordinates.x2 = ab[0] + self.w #Since the landing object isn't fixed, we are constantly updating it
        self.coordinates.y2 = ab[1] + self.h
        return self.coordinates


    def movement(self):
        if time.time() - self.lt > 0.035:#If time is greater than 0.035, last time is updated and landing position object is moved
             self.lt = time.time()
             self.game.cnvs.move(self.image, self.x, 0)
             self.cntr = self.cntr + 1
             if self.cntr > 20:#Direction gets reversed when cntr reaches 20. It now starts to move in the opposite direction
                 self.x = self.x * -1
                 self.cntr = 0

class Mario(Lists):#This class is responsible for creating Mario
    
    def __init__(self, game):
        Lists.__init__(self, game) #There are only 2 parameters since we are only dealing with Mario over here
        self.img_left = [
            PhotoImage(file="mariol1.gif"), #Each represents Mario moving in a different state moving towards left
            PhotoImage(file="mariol2.gif"),
            PhotoImage(file="mariol3.gif")
        ]
        self.img_right = [
            PhotoImage(file="marior1.gif"),#Each represents Mario moving in a different state towards right
            PhotoImage(file="marior2.gif"),
            PhotoImage(file="marior3.gif")
        ]
        self.image_splat = PhotoImage(file="mariodead.gif")
        self.image = game.cnvs.create_image(200, 470, image=self.img_left[0], anchor='nw')
        self.x = -3   #Variables responsible for changing the objects position
        self.y = 0    #when it is moving around the screen
        self.img_cur = 0 #Stores the images recent index position
        self.img_cur_add = 1  #Number to be added to the previous variable to make changes in the images current position
        self.jumpcounts = 0
        self.last_time = time.time()  #Used to obtain last time the image was changed
        self.coordinates = Coordinates() #Currently set with value 0s 
        self.distance = 0
        self.splat = False
        game.cnvs.bind_all('<KeyPress-Left>', self.left_turn)      #Binds the key to a given input from the user
        game.cnvs.bind_all('<KeyPress-Right>', self.right_turn)
        game.cnvs.bind_all('<space>', self.jump_up)
        self.dead = False#This will be used when Mario falls through a disatnce greater than 50m
        self.image_dead = PhotoImage(file="mariodead.gif")#Image of Mario Dying Loaded
    def left_turn(self, evt):#This function is called when the player presses the left arrow
        if self.y == 0:
            self.x = -3
    def right_turn(self, evt):#This function is called when the player presses the right arrow
        if self.y == 0:
            self.x = 3

    def jump_up(self, evt):#This function makes Mario jump only when he is not jumping
        if self.y == 0:#This condition checks whether mario is jumping or not
            self.y = -4
            self.jumpcounts = 0


    def motion(self):
        if self.dead:
            self.game.cnvs.itemconfig(self.image, image=self.image_dead)
            return
        if self.x != 0 and self.y == 0:#Moves Mario if it is not stationary
            if time.time() - self.last_time > 0.1:#Draws next image if time elapsed is more than 0.1s 
                self.last_time = time.time()#Resets last_time
                self.img_cur += self.img_cur_add
                if self.img_cur >= 2:#There are 3 gifs attributed to different positions, it 
                    self.img_cur_add = -1#keeps changing itself depending so that it shows that Mario is sprinting
                if self.img_cur <= 0:
                    self.img_cur_add = 1

        if self.x < 0:#Proceeds only if Mario is moving left 
            if self.y != 0:#If y is not 0, then we use the gif which shows Mario running in full stride
                self.game.cnvs.itemconfig(self.image, image=self.img_left[2])#ItemConfig is used to update the displayed image to the last image
            else:
                self.game.cnvs.itemconfig(self.image, image=self.img_left[self.img_cur])
        elif self.x > 0:#If Mario is not in full stride, then the gifs proceed accordingly
            if self.y != 0:
                self.game.cnvs.itemconfig(self.image, image=self.img_right[2])
            else:
                self.game.cnvs.itemconfig(self.image,image=self.img_right[self.img_cur])

    def coords(self):#Gets Mario's position in the game board
        ab = (self.game.cnvs.coords(self.image))#returns the x and y positions of the current image
        self.coordinates.x1 = ab[0]
        self.coordinates.y1 = ab[1]
        self.coordinates.x2 = ab[0] + 27 #Size of Mario's pixel is 27*30
        self.coordinates.y2 = ab[1] + 30
        return self.coordinates

    def movement(self):
        self.motion()
        if self.y < 0:#If it is less than 0, this means that Mario is jumping
            self.jumpcounts += 1
        if self.jumpcounts > 20:#If the value reaches 20, we need to change the 4, to make Mario fall again
            self.y = 4
        if self.y > 0: #If it is greater than 0, we need to retrace back again
            self.jumpcounts -= 1

        a = self.coords()#Tells Mario is on the screen
        left,right,top,bottom,fall = True,True,True,True,True#Everything is set to True initially     
        if self.y > 0 and a.y2 >= self.game.cnvs_height:#The following if-else clause checks whether Mario has hit bottom or top of the canvas
            self.y = 0
            bottom = False
        elif self.y < 0 and a.y1 <= 0:
            self.y = 0
            top = False

        if self.x > 0 and a.x2 >= self.game.cnvs_width:#The following if-else clause whether Mario has hit sides of the canvas
            self.x = 0
            right = False
        elif self.x < 0 and a.x1 <= 0:
            self.x = 0
            left = False

        for x in self.game.lists:#Checks whether it has hit anything else on the screen
            if x == self:
                continue#This shows that Mario has hit himself, so we move on
            allo = x.coords()#We get coordinates of new object in the list and checks whether top of Mari is in contact with another object in the given list 
            if top and self.y < 0 and top_collision(a, allo):
                self.y = -self.y
                top = False

            if bottom and self.y>0 and bottom_collision(self.y,a,allo):#y greater than 0 chechks if Mario is falling, bottom_collision checks if Mario has hit one of the landing objects
                self.y = allo.y1 - a.y2#The amount Mario should drop to land properly on the platform
                if self.y < 0:
                    self.y = 0 #If this is not set to zero, Mario will fly again
                bottom = False#top and bottom is set to False again, so that we don't waste our time checking again if it has collided with the top or bottom platforms
                top = False

            #The following code checks whether Mario has run off the edge of the platform
            if bottom and fall and self.y == 0 and a.y2<self.game.cnvs_height and bottom_collision(1,a,allo):#1st condition checks whether bottom is still True,2nd checks if Mario should be falling,
                fall = False#3rd condition checks whether Mario is already falling , 4th checks whether Mario has struck the bottom of the screen, 5th checks whether Mario has hit the top of the platform 

            if left and self.x < 0 and left_collison(a,allo): #We check if we should be searching for collisions and whether Mario has collided with anything
                self.x = 0
                left = False
                if x.gameover: #If Mario collides with the window, it has reached the end of the game
                    self.endwah(x)

            if right and self.x >0 and right_collison(a,allo):#Same stuff as the previous one
                self.x =0
                right = False
                if x.gameover:
                    self.endwah(x)

        if fall and bottom and self.y == 0 and a.y2<self.game.cnvs_height:#fall and bottom check whether we have collided at the bottom having gone through all the platforms
            self.y = 4#3rd conditin if true means he should start falling as Mario is floating in air, if y is set to 4, Mario falls off any platform
        if self.y > 0:#This code keeps updating the distance Mario falls through
            self.distance = self.distance+1
        elif self.distance > 60:#If Mario falls through a distance greater than 60 PIXELS, Mario dies
            self.distance = 0
            self.dead = True
            self.motion()
            self.game.run2 = False
            self.game.cnvs.create_text(220, 250, text=' Game Over', font=('Times', 60), fill = 'Orange')
        else:
            self.distance = 0
        self.game.cnvs.move(self.image, self.x, self.y)


    def endwah(self, x):
        self.game.run = False
        x.openwindow()
        time.sleep(1)
        self.game.cnvs.itemconfig(self.image, state='hidden')
        x.closewindow()

    

class Windows(Lists):
    def __init__(self,gamewah,x,y,w,h):#pic is the window picture that I am importing
        Lists.__init__(self,gamewah)
        self.closed_window = PhotoImage(file = "windowclosed.gif")
        self.open_window = PhotoImage(file = "windowopen.gif")
        self.image = gamewah.cnvs.create_image(x,y,image = self.closed_window,anchor = 'nw')#The image which was imported is now drawn on the screen 
        self.coordinates = Coordinates(x,y,x+(w/2),y+h)#w and h are width and height respectively of the window. The coordinates variable which was None has now been overwritten.. (w/2) indicates that he stops in front of the window
        self.gameover = True#If Mario reaches the window the game is over

    def openwindow(self):
        self.game.cnvs.itemconfig(self.image, image=self.open_window)
        self.game.tk.update_idletasks()#IdleTask method forces the new image to be displayed

    def closewindow(self):
        self.game.cnvs.itemconfig(self.image,image=self.closed_window)
        self.game.tk.update_idletasks()

g = GMain()
landingobj1 = LandingPos(g,PhotoImage(file = "land3.gif"),0,480,100,10)
landingobj2 = LandingPos(g,PhotoImage(file = "land3.gif"),150, 440, 100, 10)
landingobj3 = LandingPos(g,PhotoImage(file = "land3.gif"),300, 400, 100, 10)
landingobj4 = LandingPos(g,PhotoImage(file = "land3.gif"),300, 160, 100, 10)
landingobj5 = LandingPos(g,PhotoImage(file = "land2.gif"),175, 350, 66, 10)
landingobj6 = LandingPos(g,PhotoImage(file = "land2.gif"),50, 300, 66, 10)
landingobj7 = LandingPos(g,PhotoImage(file = "land2.gif"),170, 120, 66, 10)
landingobj8 = LandingPos(g,PhotoImage(file = "land2.gif"),40, 60, 86, 10)
landingobj9 = LandingPos(g,PhotoImage(file = "land1.gif"),160, 250, 50, 10)
landingobj10 = LandingPos(g,PhotoImage(file = "land2.gif"),230, 200, 66, 10)
g.lists.append(landingobj1)#Adding Landing Objects
g.lists.append(landingobj2)
g.lists.append(landingobj3)
g.lists.append(landingobj4)
g.lists.append(landingobj5)
g.lists.append(landingobj6)
g.lists.append(landingobj7)
g.lists.append(landingobj8)
g.lists.append(landingobj9)
g.lists.append(landingobj10)
window = Windows(g,45,30,40,35)
g.lists.append(window)#Adding the window
a = Mario(g)
g.lists.append(a)
g.looping()