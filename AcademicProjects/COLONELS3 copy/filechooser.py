# File: filechooser.py
# Version: 0.5 (3-Oct-18)

"""
The filechooser module implements a simple wrapper for the filedialog
class in Tkinter, which is the most common graphics package for use
with Python.
"""

try:
    import tkinter
    try:
        import tkinter.filedialog as tkFileDialog
    except Exception:
        import tkFileDialog
except Exception as e:
    print('Could not load tkinter: ' + str(e))

# Function: chooseInputFile

def chooseInputFile(dir=".", title="Open File"):
    """
    Opens a file chooser for selecting an input file.
    """
    tk = tkinter._default_root
    if tk is None:
        tk = tkinter.Tk()
        tk.withdraw()
    return tkFileDialog.askopenfilename(initialdir=dir, title=title)

# Function: chooseOutputFile

def chooseOutputFile(dir=".", title="Save File"):
    """
    Opens a file chooser for selecting an input file.
    """
    tk = tkinter._default_root
    if tk is None:
        tk = tkinter.Tk()
        tk.withdraw()
    return tkFileDialog.asksaveasfilename(initialdir=dir, title=title)

# Check for successful compilation

if __name__ == "__main__":
    print("filechooser.py compiled successfully")

