import random
import math
import pr1testing
random.seed()


def roll(): #function that rolls 1 6-sided die, returning an integer between 0 and 5
    return random.randint(0,5)

def play():
    player1 = input("Name of Player 1?")
    player2 = input("Name of Player 2?")
    score1 = 0
    score2 = 0
    last = False
    while True:
        print()
        print(player1 + ": " + str(score1) + "   " + player2 + ": " + str(score2))
        print('It is', player1 + "'s turn.")
        numDice = int(input("How many dice do you want to roll?"))
        diceTotal = 0
        diceString = ""
        i = numDice
        while i > 0:
            d = roll()
            diceTotal += d
            diceString = diceString + " "  + str(d)
            i = i-1
        print("Dice rolled: ", diceString)
        print("Total for this turn: ", str(diceTotal))
        score1 += diceTotal
        if score1 > 100 or last:
            break
        if numDice == 0:
            last = True
        print()
        print(player1 + ": " + str(score1) + "   " + player2 + ": " + str(score2))
        print('It is', player2 + "'s turn.")
        numDice = int(input("How many dice do you want to roll?"))
        diceTotal = 0
        diceString = ""
        i = numDice
        while i > 0:
            d = roll()
            diceTotal += d
            diceString = diceString + " "  + str(d)
            i = i-1
        print("Dice rolled: ", diceString)
        print("Total for this turn: ", str(diceTotal))
        score2 += diceTotal
        if score2 > 100 or last:
            break
        if numDice == 0:
            last = True
    print(player1 + ": " + str(score1) + "   " + player2 + ": " + str(score2))
    if score1 > 100:
        print(player2 + " wins.")
        return 2
    elif score2 > 100:
        print(player1 + " wins.")
        return 1
    elif score1 > score2:
        print(player1 + " wins.")
        return 1
    elif score2 > score1:
        print(player2 + " wins.")
        return 2
    else:
        print("Tie.")
        return 3

def autoplayLoud(strat1, strat2):
    #your code here
    score1 = 0
    score2 = 0
    last = False
    while True:
        print()
        print("player 1" + ": " + str(score1) + "   " + "player 2" + ": " + str(score2))
        print("It is " + "player 1" + "'s turn.")
        numDice = strat1(score1,score2,last)
        print (str(numDice) + " dice chosen.")
        diceTotal = 0
        diceString = ""
        i = numDice
        while i > 0:
            d = roll()
            diceTotal += d
            diceString = diceString + " "  + str(d)
            i = i-1
        print("Dice rolled: ", diceString)
        print("Total for this turn: ", str(diceTotal))
        score1 += diceTotal
        if score1 > 100 or last:
            break
        if numDice == 0:
            last = True
        print()
        print("player1" + ": " + str(score1) + "   " + "player2" + ": " + str(score2))
        print('It is', "player 2" + "'s turn.")
        numDice = strat2(score2,score1,last)
        print (str(numDice) + " dice chosen.")
        diceTotal = 0
        diceString = ""
        i = numDice
        while i > 0:
            d = roll()
            diceTotal += d
            diceString = diceString + " "  + str(d)
            i = i-1
        print("Dice rolled: ", diceString)
        print("Total for this turn: ", str(diceTotal))
        score2 += diceTotal
        if score2 > 100 or last:
            break
        if numDice == 0:
            last = True
    print("player 1" + ": " + str(score1) + "   " + "player2" + ": " + str(score2))
    if score1 > 100:
        print("player 2" + " wins.")
        return 2
    elif score2 > 100:
        print("player 1" + " wins.")
        return 1
    elif score1 > score2:
        print("player 1" + " wins.")
        return 1
    elif score2 > score1:
        print("player 2" + " wins.")
        return 2
    else:
        print("Tie.")
        return 3


def autoplay(strat1, strat2):
    #your code here
    score1 = 0
    score2 = 0
    last = False
    while True:
        numDice = strat1(score1,score2,last)
        diceTotal = 0
        i = numDice
        while i > 0:
            d = roll()
            diceTotal += d
            i = i-1
        score1 += diceTotal
        if score1 > 100 or last:
            break
        if numDice == 0:
            last = True
        numDice = strat2(score2,score1,last)
        diceTotal = 0
        i = numDice
        while i > 0:
            d = roll()
            diceTotal += d
            i = i-1
        score2 += diceTotal
        if score2 > 100 or last:
            break
        if numDice == 0:
            last = True
    if score1 > 100:
        return 2
    elif score2 > 100:
        return 1
    elif score1 > score2:
        return 1
    elif score2 > score1:
        return 2
    else:
        return 3

def manyGames(strat1, strat2, n):
    #your code here
    p1 = 0
    p2 = 0
    tie = 0
    i = 1
    k = 1
    while i <= n:
        if i % 2 == 0:
            l = autoplay(strat1,strat2)
            if l == 1:
                p1 = p1 + 1
            if l == 2:
                p2 = p2 + 1
            if l == 3:
                tie = tie + 1
        else:
            l = autoplay(strat2,strat1)
            if l == 1:
                p2 = p2 + 1
            if l == 2:
                p1 = p1 + 1
            if l == 3:
                tie = tie + 1
        i = i + 1
    print ("Player 1 wins : " + str(p1))
    print ("Player 2 wins : " + str(p2))
    print ("Ties          : " + str(tie))


def sample1(myscore, theirscore, last):
    if myscore > theirscore:
        return 0
    else:
       return 12

def sample2(myscore, theirscore, last):
    if myscore <= 50:
        return 30
    if myscore >= 51 and myscore <= 80:
        return 10
    if myscore > 80:
        return 0

def improve(strat1):
    #your code here
    def strat3(myscore,theirscore,last):
        if myscore == 100:
            return 0
        else:
            return strat3(myscore,theirscore,last)
    return strat3
def myStrategy(myscore, theirscore, last):
    k = myscore - theirscore
    l = theirscore - myscore
    x = 100 - myscore
    if myscore == 0:
        return 32
    if theirscore == 100 and myscore!= 100:
        return 1
    if myscore == 99 or myscore == 100:
        return 0
    if k >= 10:
        if myscore == 97 or myscore == 98:
            return 0
        if myscore >92 and myscore <= 96:
            return 1
        if myscore >= 91 and myscore <= 92:
            return 2
    if k >= 20:
        if myscore >= 80:
            return x// 3.
        if myscore >= 72:
            return x//3.40
    if k >= 1 and k <= 2 and (myscore == 97): 
         return 1 
    if k==0:
        if myscore == 98 or myscore == 1:
            return 1
    if l >= 1 and l <=3 :
            if theirscore >= 95:
                if myscore >= 91 and myscore <= 94:
                    return 2
                if myscore >= 95 and myscore <= 98:
                    return 1 
    if l >= 8:
        if theirscore >= 85:
            return x//3.1
    if l >= 4:
        if theirscore >= 92:
            if myscore == 96 or myscore == 97 or myscore == 95 or myscore == 98:
                return 1
            if myscore == 94 or myscore == 93:
                return 2
            if myscore == 91:
                return 3
        else:
            return x//3.30
    if myscore == 98:
        return 0
    if x >= 40:
        return x//2.8
    if x >= 30:
        return x//2.92
    if x >= 20:
        return x//3.06
    if x >= 10:
        return x//3.2
    if x >= 4:
        return x//3.35
    if x == 3:
        return 1