#! /usr/bin/env python3

'''
Created on Nov 22, 2012

@author: finn
'''

from random import shuffle

from Board import Board
from Resource import Resource
from Strategy import StupidBot, Human
from Player import Player, PlayerColor


class Game(object):
    '''
    class to represent the game loop
    '''

    def __init__(self):
        self.board = Board()
        self.players = []
        
    def playerCount(self):
        return len(self.players)
    
    def addPlayer(self, player):
        self.players.append(player)
    
    def allPersonsPlaced(self):
        return sum([player.personsLeft(self.board) for player in self.players]) == 0
    
    def processRound(self):
        for player in self.players:
            player.newRound()
        while not self.allPersonsPlaced():
            for player in [p for p in self.players if p.personsLeft(self.board) > 0]:
#                 print("Player: %-6s to place persons" % (player.getOutputColor()))                
                if isinstance(player.strategy, Human):                
                    print (self.board)  
                player.placePersons(self.board)
                
        print("Player: %-6s to reap resources " % (player.getOutputColor()))
        for idx, player in enumerate(self.players): # reap resources and buy building tiles
            if isinstance(player.strategy, Human):                                    
                print (self.board)
            activeFirst = self.players[idx:] + self.players[:idx]
            huts, cards = self.board.reapResources(activeFirst)
            
            boughtCards = player.buyCards(cards, activeFirst, self.board.cardPile)
            self.board.removeCards(boughtCards)
            
            boughtHuts = player.buyHuts(huts)
            self.board.popHuts(boughtHuts)
            
            if isinstance(player.strategy, Human):                        
                print(player)
        
        for player in self.players: # feed and adjust score
            player.feed()
            
        # cycle player sequence
        self.players = self.players[1:] + self.players[:1]  

    def finished(self):
        return self.board.isFinished()
    
    def getPlayers(self):
        return sorted(self.players[:], reverse = True)

    def doPrintPlayers(self, heading, scoreFunc):
        print(heading)
        maximalColorLength = max(len(player.getColor().name) for player in self.players)
        for player in self.getPlayers():
            print("%s : %s (%s)"  % (player.getOutputColor(maximalColorLength), scoreFunc(player) , player.getStrategy()))            
    
    def printPlayers(self):
        self.doPrintPlayers("Players:", lambda p: "")

    def printScores(self):
        self.doPrintPlayers("Scores:", lambda p: "%3d" % p.getScore())

    def printFinalScores(self):
        self.doPrintPlayers("\n\nFinal scores:", lambda p: "%3d, second criteria: %2d" % (p.getScore(), p.secondScoreCriteria()))

def main():
    game = Game()
    game.addPlayer(Player(PlayerColor.Red, StupidBot()))
    game.addPlayer(Player(PlayerColor.Blue,  StupidBot()))
    game.addPlayer(Player(PlayerColor.Green,  Human(game.printScores)))
    game.addPlayer(Player(PlayerColor.Yellow,  StupidBot()))
    shuffle(game.players)
    game.printPlayers()
    gameRound = 1
    try:
        while not game.finished():
            input("Press the return key to proceed to the next round....")
            print("\nRound: %d" % (gameRound))
            game.processRound()
            gameRound +=1
            game.printScores()
        game.printFinalScores()
    except KeyboardInterrupt:
        game.printFinalScores()     
        print("\nbye and see you soon!")

if __name__ == '__main__':
    main()
