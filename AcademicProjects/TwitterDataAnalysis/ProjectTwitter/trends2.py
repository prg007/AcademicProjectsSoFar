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
    #your code here
    return tweet['text']

def tweet_time(tweet):
    """Return the datetime representing when a tweet was posted."""
    #your code here
    return tweet['time']
def tweet_location(tweet):
    """Return a position representing a tweet's location."""
    #your code here
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
    #your code here
    lat1=latitude(segstart)
    lat2=latitude(segend)
    long1=longitude(segstart)
    long2=longitude(segend)
    lat3=latitude(point)
    long3=longitude(point)
    slope= (long2-long1)/(lat2-lat1)
    c=long1-slope*lat1 
    if long3==slope*lat3+c:
        return True
    else:
        return False


def is_in_state(point, state):
    """Finds if a point (position) is inside a state (list of polygons).
    Uses the ray casting algorithm at http://en.wikipedia.org/wiki/Point_in_polygon
    Whether a side intersects the ray is checked with check_intersect """
    #your code here
    n=0
    x=0
    while x<len(state):
        y=0
        while y<(len(state(x)-1)):
            if check_intersect(point, state(x)(y),state(x)(y+1)):
                n=n+1


    if n%2==0:
        return False
    else:
        return True 

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
    #your code here
    newdict={}
    for f in us_states:
        newdict[us_states(f)]=0
    for i in us_states:
        for j in tweets:
            if is_in_state(tweet_location(tweets(j)),us_states(i)):
                newdict[us_states(i)]=newdict[us_states(i)]+1

    for i in us_states:
        newdict[us_states(i)]=newdict[us_states(i)]/us_state_pop[us_state(i)]
    m=1
    while m<len(newdict):
        max1=max(newdict[us_states(m),us_states(m-1)])
        m+=1
    for i in us_states:    
        newdict[us_states(i)]=newdict[us_states(i)]/max1
    return newdict


####################
# Phase 4: Queries #
####################

def canada_query(text):
    """Return True if text contains "canada" as a substring.
    Results should not be case-sensitive.  When text includes "CAnada", 
    for example, should return True.
    """
    #your code here
    counter=0
    while counter<=(len(text)-5):
        if text[counter:counter+5].lower()=='canada':
            return True
        counter+=1


def make_searcher(term):
    """Returns a test that searches for term as a substring of a given string.
    Results should not be case-sensitive.
    For example, makesearcher("canada") should behave identically to canada_query.
    """
    #your code here
    counter=0
    while counter<=(len(tweet_text(text))-(len(term)-1)):
        if tweet_text(text)[counter:counter+5].lower()==term:
            return True

def mexico_query(text):
    """Returns true if "mexico" is included as a substring and "new" is not.
    Again, results should not be case-sensitive.
    """
    #your code here
    if make_searcher('mexico') and not make_searcher('new'):
        return True


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

# Uncomment (and edit) the line below to create a map based on a query of your choice
#draw_map_for_query(canada_query)