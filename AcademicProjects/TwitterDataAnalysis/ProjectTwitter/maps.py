"""Map drawing utilities for U.S. tweet data."""

from graphics import Canvas
from geo import position_to_xy, us_states

# A fixed gradient of frequency colors from low (pale blue) to high (dark blue)
# Colors chosen via Cynthia Brewer's Color Brewer (colorbrewer2.com)
FREQUENCY_COLORS = ["#f7fbff", "#deebf7", "#c6dbef", "#9ecae1", "#6baed6",
                    "#4292c6", "#2171b5", "#08519c", "#08306b"]
GRAY = "#AAAAAA"

def get_frequency_color(frequency, frequency_scale=1):
    """Returns a color corresponding to the frequency value.

    frequency -- a number between 0 and +1
    """
    if frequency is None:
        return GRAY
    scaled = frequency_scale * frequency
    index = int( scaled * len(FREQUENCY_COLORS) ) # Rounds down
    if index < 0:
        index = 0
    if index >= len(FREQUENCY_COLORS):
        index = len(FREQUENCY_COLORS) - 1
    return FREQUENCY_COLORS[index]

def draw_state(shapes, frequency_value=None):
    """Draw the named state in the given color on the canvas.

    state -- a list of list of polygons (which are lists of positions)
    frequency_value -- a number between 0 and 1 (positive)
    canvas -- the graphics.Canvas object
    """
    for polygon in shapes:
        vertices = [position_to_xy(position) for position in polygon]
        color = get_frequency_color(frequency_value)
        get_canvas().draw_polygon(vertices, fill_color=color)

def draw_dot(location, frequency_value=None, radius=3):
    """Draw a small dot at location.

    location -- a position
    frequency_value -- a number between 0 and 1 (positive)
    """
    center = position_to_xy(location)
    color = get_frequency_color(frequency_value)
    get_canvas().draw_circle(center, radius, fill_color=color)

def memoize(fn):
    """A decorator for caching the results of the decorated function."""
    cache = {}
    def memoized(*args):
        if args in cache:
            return cache[args]
        result = fn(*args)
        cache[args] = result
        return result
    return memoized

@memoize
def get_canvas():
    """Return a Canvas, which is a drawing window."""
    return Canvas(width=960, height=500)

def wait(secs=0):
    """Wait for mouse click."""
    get_canvas().wait_for_click(secs)

def message(s):
    """Display a message."""
    c = get_canvas()
    c.draw_text(s, (c.width//2, c.height//2), size=36, anchor='center')
