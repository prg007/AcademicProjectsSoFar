# File: mazelib.py

"""
This module exports tools for working with mazes.
"""

from pgl import GCompound, GRect

# Class: Maze

class Maze(GCompound):
    """
    This class represents a maze that can be displayed in a graphics window.
    The maze keeps track of a two-dimensional array of rooms (nRows x nCols)
    and the walls that separate those rooms.
    """   

    def __init__(self, nRows, nCols, sqSize):
        """
        Creates a new Maze object with the specified number of rows and
        columns and in which each square has the specified size.  The
        return value is a single graphical object descended from GCompound
        that can be added to a GWindow.  In keeping with the conventions
        of the Portable Graphics Library, the reference point for the
        Maze object is its upper left corner.
        """
        GCompound.__init__(self)
        self._nRows = nRows
        self._nCols = nCols
        self._sqSize = sqSize
        self._addGrid(nRows, nCols, sqSize)
        self._addVerticalWalls(nRows, nCols, sqSize)
        self._addHorizontalWalls(nRows, nCols, sqSize)
        self._addBorders(nRows, nCols, sqSize)
        self._addIntersections(nRows, nCols, sqSize)
        

    def __str__(self):
        """Converts a Maze object to a string."""
        return "<Maze(" + str(self.nCols) + "x" + str(self.nCols) + ")"

    def getSquares(self):
        """Returns a list of all the maze squares in row-major order."""
        squares = [ ]
        for row in self._grid:
            for sq in row:
                squares.append(sq)
        return squares

    def getSquare(self, row, col):
        """Returns the square at the specified row and column."""
        return self._grid[row][col]

    def getWalls(self):
        """Returns a list of all the walls."""
        walls = [ ]
        for wall in self._verticalWalls.values():
            walls.append(wall)
        for wall in self._horizontalWalls.values():
            walls.append(wall)
        return walls

    def getWall(self, sq1, sq2):
        """Returns the wall between sq1 and sq2."""
        if sq1._row == sq2._row and sq1._col + 1 == sq2._col:
            return self._verticalWalls[(sq1._row, sq1._col)]
        elif sq1._row + 1 == sq2._row and sq1._col == sq2._col:
            return self._horizontalWalls[(sq1._row, sq1._col)]
        else:
            raise ValueError("Wall does not connect adjacent squares")

# Implementation notes: Private methods
# -------------------------------------
# The methods that follow are private to the Maze class.  These methods
# break down the initialization of the maze into phases to avoid having
# all the code in one monolithic function.  The squares are stored in
# a two-dimensional array indexed by the row and column numbers.  The
# walls are stored in two dictionaries -- one for vertical walls and
# one for horizontal walls -- for which the keys are a tuple composed
# of the coordinates of the square to the left of a vertical wall or
# the square above a horizontal wall.

    def _addGrid(self, nRows, nCols, sqSize):
        """Adds the grid of squares to the maze."""
        self._grid = [ ]
        for i in range(nRows):
            y = i * sqSize
            row = [ ]
            for j in range(nCols):
                x = j * sqSize
                sq = MazeSquare(i, j, sqSize)
                self.add(sq, x, y)
                row.append(sq)
            self._grid.append(row)

    def _addVerticalWalls(self, nRows, nCols, sqSize):
        """Adds the vertical walls to the maze."""
        self._verticalWalls = { }
        for i in range(nRows):
            y = i * sqSize
            for j in range(1, nCols):
                x = j * sqSize
                sq1 = self._grid[i][j - 1]
                sq2 = self._grid[i][j]
                wall = MazeWall(sq1, sq2, sqSize)
                self._verticalWalls[(i,j)] = wall
                self.add(wall, x, y)

    def _addHorizontalWalls(self, nRows, nCols, sqSize):
        """Adds the horizontal walls to the maze."""
        self._horizontalWalls = { }
        for i in range(1, nRows):
            y = i * sqSize
            for j in range(nCols):
                x = j * sqSize
                sq1 = self._grid[i - 1][j]
                sq2 = self._grid[i][j]
                wall = MazeWall(sq1, sq2, sqSize)
                self._horizontalWalls[(i,j)] = wall
                self.add(wall, x, y)

    def _addBorders(self, nRows, nCols, sqSize):
        """Adds the maze borders, leaving gaps for entrance and exit."""
        self.add(GFilledRect(sqSize, 0, (nCols - 1) * sqSize + 2, 2))
        self.add(GFilledRect(0, nRows * sqSize, (nCols - 1) * sqSize + 2, 2))
        self.add(GFilledRect(0, 0, 2, nRows * sqSize + 2))
        self.add(GFilledRect(nCols * sqSize, 0, 2, nRows * sqSize + 2))

    def _addIntersections(self, nRows, nCols, sqSize):
        """Adds the 2x2 squares that sit at the intersections."""
        for i in range(1, nRows):
            y = i * sqSize
            for j in range(1, nCols):
                x = j * sqSize
                self.add(GFilledRect(x, y, 2, 2))

# Class: MazeSquare

class MazeSquare(GRect):
    """
    This class represents an individual square in a maze.
    """   

    def __init__(self, row, col, sqSize):
        GRect.__init__(self, sqSize, sqSize)
        self.setFilled(True)
        self.setColor("White")
        self._row = row
        self._col = col
        self._link = None
        self._rank = 0

    def __str__(self):
        """Converts the square to a string representing its coordinates."""
        return chr(ord("a") + self._col) + str(self._row)

# Implementation notes: setColor and getColor
# -------------------------------------------
# Even though setColor and getColor are inherited from the GRect class,
# these methods are overridden here to ensure that the values returned
# by getColor are the same as those provided in the last setColor call.
# In the base class, calling getColor on a GRect object after calling
# setColor("Red") would return "#FF0000", which is the hex encoding of
# the color.

    def setColor(self, color):
        """Sets the color of the square to the specified string."""
        GRect.setColor(self, color)
        self._color = color

    def getColor(self):
        """Returns the color string from the most recent setColor call."""
        return self._color

    def getRow(self):
        """Returns the horizontal row for this square."""
        return self._row

    def getCol(self):
        """Returns the vertical column for this square."""
        return self._col

# Implementation notes: setLink and getLink
# -----------------------------------------
# These methods are not used in the base implementation but provide
# access to a link field in each MazeSquare object that can be used
# to keep track of the link to its parent in the union-find algorithm.

    def setLink(self, link):
        """Sets the link field for this square."""
        self._link = link

    def getLink(self):
        """Returns the link field for this square."""
        return self._link

# class MazeWall

class MazeWall(GRect):

    def __init__(self, sq1, sq2, sqSize):
        """Creates a wall between sq1 and sq2."""
        if sq1._row == sq2._row and sq1._col + 1 == sq2._col:
            GRect.__init__(self, 2, sqSize + 2)
        elif sq1._row + 1 == sq2._row and sq1._col == sq2._col:
            GRect.__init__(self, sqSize + 2, 2)
        else:
            raise ValueError("Wall does not connect adjacent squares")
        self._sq1 = sq1
        self._sq2 = sq2
        self.setFilled(True)
        self.setColor("LightGray")

    def __str__(self):
        """Returns a string consisting of the coordinates on each side."""
        return str(self._sq1) + "-" + str(self._sq2)

    def getSquares(self):
        """Returns a tuple of the squares separated by this wall."""
        return (self._sq1, self._sq2)

class GFilledRect(GRect):
    """This class represents a rectangle that is filled by default."""

    def __init__(self, x, y, width, height, color="Black"):
        GRect.__init__(self, x, y, width, height)
        self.setFilled(True)
        self.setColor(color)
