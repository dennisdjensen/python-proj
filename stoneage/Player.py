'''
Created on Nov 22, 2012

@author: finn
'''

from functools import total_ordering
from enum import Enum

from Toolbox import Toolbox
from Card import SymbolCard, MultiplierCard, CardMultiplier
from Resource import Resource

class PlayerColor(Enum):
    Red = '\x1b[1;31m'
    Green = '\x1b[1;32m'
    Yellow = '\x1b[2;33m'
    Blue = '\x1b[1;34m'

@total_ordering
class Player():
    '''
    classdocs
    '''
    
    maxFoodTrack   = 10
    maxPersonCount = 10
    hungerPenalty  = -10
    colorOSnormal  = '\x1b[0m'

    def __init__(self, color, strategy):
        self.resources = 12 * [Resource.food]
        self.huts = []
        self.cards = []
        self.person = 5
        self.score = 0
        self.color = color
        self.playerAbr = color.name[:1].lower()
        self.colorOS = color.value
        self.strategy = strategy
        self.farmer = 0
        self.toolbox = Toolbox()
        self.oneTimeTools = []
        
    def __lt__(self, other):
        if self.getScore() != other.getScore():
            return self.getScore() < other.getScore()
        return  self.secondScoreCriteria() < other.secondScoreCriteria()  

    def __eq__(self, other):
        return self is other
    
    def __hash__(self):
        return hash("".join([o.__str__() for o in [self.getColor(), self.strategy]]))

    def getFoodTrack(self):
        return self.farmer

    def getTools(self):
        return self.toolbox.getTools()

    def getPersonCount(self):
        return self.person

    def foodMissing(self):
        return max(0, (self.person - self.farmer) - self.resources.count(Resource.food))
    
    def feed(self):
        if self.foodMissing() > 0 :
            self.score += self.hungerPenalty
        for person in range((self.person - self.farmer) - self.foodMissing()): 
            self.resources.remove(Resource.food)

    def getFood(self):
        return [resource for resource in self.resources if resource == Resource.food]
    
    def getNonFood(self):
        return sorted([resource for resource in self.resources if resource != Resource.food])

    def addResources(self, additionalResources):
        while Resource.tool in additionalResources: 
            self.toolbox.upgrade()
            additionalResources.remove(Resource.tool)
        while Resource.farmer in additionalResources: 
            self.farmer = min(self.maxFoodTrack, self.farmer + 1)
            additionalResources.remove(Resource.farmer)
        while Resource.person in additionalResources: 
            self.person = min(self.maxPersonCount, self.person + 1)
            additionalResources.remove(Resource.person)
        self.resources.extend(additionalResources)
        
    def addOneTimeTool(self, value):
        self.oneTimeTools.append(value)
        
    def removeResources(self, resourcesToRemove):
        for resource in resourcesToRemove:
            self.resources.remove(resource)
        
    def buyHuts(self, huts):
        return self.strategy.buyHuts(self, huts)

    def buyHut(self, hut, payment):
        self.huts.append(hut)
        self.executeHutPayment(payment)

    def isPayable(self, hut):
        return self.strategy.isPayable(hut, self.resources)

    def executeHutPayment(self, payment):
        self.removeResources(payment)
        self.score += sum(payment)

    def addCard(self, card, players, cardPile):
        self.cards.append(card)
        card.execute(players, cardPile)
   
    def getCardScore(self):
        symbolList = {}
        for card in [c for c in self.cards if isinstance(c, SymbolCard)]:
            if not card.getSymbol() in symbolList.keys():
                symbolList[card.getSymbol()] = []
            symbolList[card.getSymbol()].append(card)
        
        points1 = pow(len(symbolList.keys()), 2)
        points2 = pow(len([lst for lst in symbolList.values() if len(lst) == 2]), 2)
        
        mulitplierPoints = 0
        for card in [c for c in self.cards if isinstance(c, MultiplierCard)]:
            if card.getSymbol() == CardMultiplier.hutBuilder:
                mulitplierPoints += card.getMultiplier() * len(self.huts)
            elif card.getSymbol() == CardMultiplier.farmer:
                mulitplierPoints += card.getMultiplier() * self.farmer
            elif card.getSymbol() == CardMultiplier.toolMaker:
                mulitplierPoints += card.getMultiplier() * sum(self.toolbox.getTools())
            elif card.getSymbol() == CardMultiplier.shaman:
                mulitplierPoints += card.getMultiplier() * self.person

        return points1 + points2 + mulitplierPoints
       
    def addScore(self, score):
        self.score += score

    def getScore(self):
        return self.score + self.getCardScore() + len(self.getNonFood())
    
    def secondScoreCriteria(self):
        return self.farmer + sum(self.toolbox.getTools()) + self.person
    
    def personsLeft(self, board):
        return self.person - board.person(self)

    def isNewRound(self, board):
        return self.personsLeft(board) == self.person

    def placePersons(self, board):
        self.strategy.placePersons(self, board)
        
    def chooseChristmas(self, presents):
        return self.strategy.chooseChristmas(self, presents)
    
    def getColor(self):
        return self.color

    def getOutputColor(self):
        return "%s%s%s" %  (self.colorOS, self.color.name, self.colorOSnormal)

    def getAbr(self):
        return self.playerAbr

    def getOutputAbr(self):
        return "%s%s%s" %  (self.colorOS, self.playerAbr, self.colorOSnormal)
    
    def toolsToUse(self, resource, eyes): 
        return self.strategy.toolsToUse(resource, eyes, self.toolbox)
    
    def newRound(self):
        self.toolbox.reset()
    
    def getStrategy(self):
        return self.strategy
    
    def chooseReapingResource(self, occupiedResources):
        return self.strategy.chooseReapingResource(occupiedResources)
    
    def resourcesColoredOutput(self):
        return "[%s]" % ",".join([resource.getColoredName() for resource in sorted(self.getNonFood())])
    
    def __str__(self):
        return """%s%s%s
People: %d, Foodtrack: %d, Food: %d, Tools: %s
Resources: %s
huts: %s    
score: %d\n""" % (self.colorOS, self.color.name, self.colorOSnormal, self.getPersonCount(), self.getFoodTrack(), self.resources.count(Resource.food), self.toolbox, 
                  Resource.coloredOutput(sorted(self.getNonFood())), 
                  ",".join([str(hut) for hut in self.huts]), self.getScore())

