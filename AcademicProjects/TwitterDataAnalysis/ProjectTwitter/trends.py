"""Visualizing Twitter Topics Across America"""

from data import load_tweets
from datetime import datetime
from geo import us_states, us_state_pop, geo_distance, make_position, longitude, latitude
from maps import draw_state, wait
import random


################################
# Phase 1: Working With Tweets #
################################

# The tweet abstract data type, implemented as a dictionary.

def make_tweet(text, time, lat, lon):
    """Return a tweet, represented as a Python dictionary.

    text  -- A string; the text of the tweet, all in lowercase
    time  -- A datetime object; the time that the tweet was posted
    lat   -- A number; the latitude of the tweet's location
    lon   -- A number; the longitude of the tweet's location

    >>> t = make_tweet("just ate lunch", datetime(2012, 9, 24, 13), 38, 74)
    >>> tweet_text(t)
    'just ate lunch'
    >>> tweet_time(t)
    datetime.datetime(2012, 9, 24, 13, 0)
    >>> p = tweet_location(t)
    >>> latitude(p)
    38
    >>> tweet_string(t)
    '"just ate lunch" @ (38, 74)'
    """
    return {'text': text, 'time': time, 'latitude': lat, 'longitude': lon}

def tweet_text(tweet):
    """Return a string, the words in the text of a tweet."""
    
    return tweet['text']

def tweet_time(tweet):
    """Return the datetime representing when a tweet was posted."""
    
    return tweet['time']
def tweet_location(tweet):
    """Return a position representing a tweet's location."""
    
    return make_position(tweet['latitude'],tweet['longitude'])
def tweet_string(tweet):
    """Return a string representing a functional tweet."""
    location = tweet_location(tweet)
    point = (latitude(location), longitude(location))
    return '"{0}" @ {1}'.format(tweet_text(tweet), point)


#################################
# Phase 2: The Geometry of Maps #
#################################

def check_intersect(point, segstart, segend):
    """Takes three positions, a point and two endpoints of a line 
    segment. Checks whether the ray pointing due east from 
    point goes through the line segment from segstart to segend"""
   
    if ((point[1] < segstart[1]) and (point[1] > segend[1])) or ((point[1] > segstart[1]) and (point[1] < segend[1])):
        x = (point[1] - segstart[1]) * ((segstart[0] - segend[0]))/(segstart[1] - segend[1]) + segstart[0]
        if point[0] < x:
            return True
        else :
            return False
    else :
        return False


def is_in_state(point, state):
    """Finds if a point (position) is inside a state (list of polygons).
    Uses the ray casting algorithm at http://en.wikipedia.org/wiki/Point_in_polygon
    Whether a side intersects the ray is checked with check_intersect """
    for x in state:
        counter = 0
        j = 0
        while j < len(x):
            if j + 1 == len(x):
                if check_intersect(point,x[j],x[0]) == True:
                    counter += 1
            elif check_intersect(point,x[j],x[j+1]) == True:
                counter += 1
            j += 1
        if counter%2 != 0:
            return True
        else:
            return False
        
#####################################
# Phase 3: The Tweets of the Nation #
#####################################

def count_tweets_by_state(tweets):
    """Return a dictionary that aggregates tweets by their state of origin.

    The keys of the returned dictionary are state names, and the values are
    normalized per capita tweet frequencies. You may use the dictionary
    us_state_pop, which associates state abbreviation keys with 2013 estimated
    population for the given state.

    tweets -- a sequence of tweet abstract data types
    """
    
    newdict={}
    state = list(us_states.keys())
    p = 0
    while p < len(state):
        newdict[state[p]] = 0
        p = p + 1
    elm = 0
    while elm < len(tweets):
        x = tweet_location(tweets[elm])
        for i,j in us_states.items():
            if is_in_state(x,us_states[i]) == True:
                newdict[i] += 1
        elm += 1

    for k,v in newdict.items():
        newdict[k] = newdict[k] / us_state_pop[k]

    x = newdict['IL']
    for k,v in newdict.items():
        y = max(newdict[k],x)
        if y > x:
            x = y

    for k,v in newdict.items():
        if x == 0:
            return newdict
        else:
            newdict[k] = newdict[k]/x

    return newdict

####################
# Phase 4: Queries #
####################

def canada_query(text):
    """Return True if text contains "canada" as a substring.
    Results should not be case-sensitive.  When text includes "CAnada", 
    for example, should return True.
    """
  
    counter=0
    while counter<len(text):
        if text[counter:counter+6].lower()=='canada':
            return True
        counter+=1
    return False

def make_searcher(term):
    """Returns a test that searches for term as a substring of a given string.
    Results should not be case-sensitive.
    For example, makesearcher("canada") should behave identically to canada_query.
    """
   
    def x(text):
        counter=0
        k = len(term)
        p = len(text)
        while counter<p:
            if  text[counter:counter+k].lower()==term:
                return True
            counter = counter + 1
        return False
    return x

def mexico_query(text):
    """Returns true if "mexico" is included as a substring and "new" is not.
    Again, results should not be case-sensitive.
    """
   
    counter = 0
    while counter<len(text):
        if text[counter:counter+6].lower()=='mexico':
            j = 0
            while j<len(text):
                if text[j:j+3].lower()=='new':
                    return False
                j = j + 1
            return True
        counter+=1
    return False




#########################
# Map Drawing Functions #
#########################

def draw_state_frequencies(state_frequencies):
    """Draw all U.S. states in colors corresponding to their frequency value."""
    for name, shapes in us_states.items():
        frequency = state_frequencies.get(name, None)
        draw_state(shapes, frequency)

def draw_map_for_query(test, new_file_name=None):
    if new_file_name == None:
        random.seed()
        new_file_name = str(random.randint(0, 1000000000))
    """Draw the frequency map corresponding to the tweets that pass the test.
    """
    tweets = load_tweets(make_tweet, test, new_file_name)
    tweets_by_state = count_tweets_by_state(tweets)
    draw_state_frequencies(tweets_by_state)
    wait()



#################################
# Phase 5: Use what you've done #
#################################

draw_map_for_query(make_searcher('gravity'))
