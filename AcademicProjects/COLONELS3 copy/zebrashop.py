# File: ImageShop.py

"""
This program is the starter file for the ImageShop application, which
implements the "Load" and "Flip Vertical" buttons.
"""

from filechooser import chooseInputFile
from pgl import GWindow, GImage, GRect, GButton, GLabel
import sys

# Constants

GWINDOW_WIDTH = 1024
GWINDOW_HEIGHT = 700
BUTTON_WIDTH = 125
BUTTON_HEIGHT = 20
BUTTON_MARGIN = 10
BUTTON_BACKGROUND = "#CCCCCC"
LUMINANCE_LEVELS = 256

# Derived constants

BUTTON_AREA_WIDTH = 2 * BUTTON_MARGIN + BUTTON_WIDTH
IMAGE_AREA_WIDTH = GWINDOW_WIDTH - BUTTON_AREA_WIDTH

def luminance(pixel):
    """
    Returns the luminance of a pixel, which indicates its subjective
    brightness.  This implementation uses the NTSC formula.
    """
    r = GImage.getRed(pixel)
    g = GImage.getGreen(pixel)
    b = GImage.getBlue(pixel)
    return round(0.299 * r + 0.587 * g + 0.114 * b)

# The ImageShop application

def ImageShop(classifier_file):
    def addButton(label, action):
        """
        Adds a button to the region on the left side of the window
        """
        nonlocal nextButtonY
        x = BUTTON_MARGIN
        y = nextButtonY
        button = GButton(label, action)
        button.setSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        gw.add(button, x, y)
        nextButtonY += BUTTON_HEIGHT + BUTTON_MARGIN

    def setImage(image):
        """
        Sets image as the current image after removing the old one.
        """
        nonlocal currentImage
        if currentImage is not None:
            gw.remove(currentImage)
        currentImage = image
        x = BUTTON_AREA_WIDTH + (IMAGE_AREA_WIDTH - image.getWidth() * image.sf) / 2
        y = (gw.getHeight() - image.getHeight() * image.sf) / 2
        gw.add(image, x, y)

    def setThermometer(percentage):
        if percentage > 0.50:
            showYes()
        else:
            showNo()
        likelihood.setSize(BUTTON_AREA_WIDTH-10,
                           percentage * (GWINDOW_HEIGHT-nextButtonY-5))

    def loadButtonAction():
        """Callback function for the Load button"""
        nonlocal currentFile
        filename = chooseInputFile()
        currentFile = filename
        if filename != "":
            img = GImage(filename)
            width = len(img.getPixelArray())
            height = len(img.getPixelArray()[0])
            max_dim = max(width, height)
            sf = 750 / max_dim
            if max_dim > 750:
                img.scale(sf)
            
            setImage(img)
            clearMessage()

    def flipVerticalAction():
        """Callback function for the FlipVertical button"""
        if currentImage is not None:
            setImage(flipVertical(currentImage))

    def flipHorizontalAction():
        """Callback function for the FlipHorizontal button"""
        if currentImage is not None:
            setImage(flipHorizontal(currentImage))

    def rotateLeftAction():
        """Callback function for the RotateLeft button"""
        if currentImage is not None:
            setImage(rotateLeft(currentImage))

    def rotateRightAction():
        """Callback function for the RotateRight button"""
        if currentImage is not None:
            setImage(rotateRight(currentImage))



    def isZebraAction():
        """Callback function for the Is It a Zebra? button"""
        if currentFile is not None:
            zebra_prob = classifier(currentFile)['zebra']
            setThermometer(zebra_prob)
  
    def showYes():
        clearMessage()
        gw.add(yes, BUTTON_AREA_WIDTH//2-30, GWINDOW_HEIGHT-nextButtonY//2-150)
                  
    def showNo():
        clearMessage()
        gw.add(no, BUTTON_AREA_WIDTH//2-20, GWINDOW_HEIGHT-nextButtonY//2-150)

    def clearMessage():
        gw.remove(yes)        
        gw.remove(no)
        
    gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT)
    buttonArea = GRect(0, 0, BUTTON_AREA_WIDTH, GWINDOW_HEIGHT)    
    buttonArea.setFilled(True)
    buttonArea.setColor(BUTTON_BACKGROUND)
    gw.add(buttonArea)
    nextButtonY = BUTTON_MARGIN
    currentImage = None
    currentFile = None
    addButton("Load", loadButtonAction)
    addButton("Flip Vertical", flipVerticalAction)
    addButton("Flip Horizontal", flipHorizontalAction)
    addButton("Rotate Left", rotateLeftAction)
    addButton("Rotate Right", rotateRightAction)
    addButton("Is It a Zebra?", isZebraAction)
    thermometer = GRect(5, nextButtonY, BUTTON_AREA_WIDTH-10, GWINDOW_HEIGHT-nextButtonY-5)    
    thermometer.setFilled(True)
    thermometer.setColor("red")
    likelihood = GRect(5, nextButtonY, BUTTON_AREA_WIDTH-10, 0)    
    likelihood.setFilled(True)
    likelihood.setColor("green")
    gw.add(thermometer)    
    gw.add(likelihood)        
    yes = GLabel("YES")
    yes.setColor("white")
    yes.setFont("bold 36px 'Monaco','Monospaced'")
    no = GLabel("NO")
    no.setColor("white")
    no.setFont("bold 36px 'Monaco','Monospaced'")

    from cnn import Classifier

    classifier = Classifier.load(classifier_file)
    


# Creates a new GImage from the original one by flipping it vertically.

def flipVertical(image):
    array = image.getPixelArray()
    return GImage(array[::-1])

def flipHorizontal(image):
    array = image.getPixelArray()
    return GImage([row[::-1] for row in array])

def rotateLeft2(image):
    array = image.getPixelArray()
    width = image.getWidth()
    return GImage([[row[i] for row in array] for i in range(width)][::-1])

def rotateLeft(image):
    array=image.getPixelArray()
    newArray=[[0]*len(array) for i in range(len(array[0]))]
    for col in range(len(newArray[0])):
        for row in range(len(newArray)):
            newArray[row][col]=array[col][len(array[0])-1-row]
    return GImage(newArray)

def rotateRight(image):
    for i in range(3):
        image = rotateLeft(image)
    return image
   
    
          


# Startup code

if __name__ == "__main__":
    classifier_file = sys.argv[1]
    ImageShop(classifier_file)
