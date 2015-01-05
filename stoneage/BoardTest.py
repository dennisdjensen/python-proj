#! /usr/bin/env python3

import unittest
from Board import Board
from Hut import Hut, SimpleHut
from Player import Player
from Strategy import StupidBot

class BoardTest(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.redPlayer = Player("Red", StupidBot())
        self.bluePlayer = Player("Blue", StupidBot())
        self.players = [self.redPlayer, self.bluePlayer]

    def testBoardInitialization(self):
        self.assertListEqual([7,7,7,7], self.board.numberOfHutsLeft())
        self.assertEqual(36, self.board.numberOfCardsLeft())

    def testAvailableHuts(self):
        ahs = self.board.availableHuts()
        self.assertEqual(4, len(ahs))
        self.assertIsInstance(ahs[0], Hut)
    
    def testPlaceOnHut(self):
        ahs = self.board.availableHuts()
        targetHut = ahs[0]
        self.board.placeOnHutIndex(0, self.redPlayer)
        ahs = self.board.availableHuts()
        self.assertEqual(3, len(ahs), "should only be 3 huts left")
        self.assertNotIn(targetHut, ahs, "hut should not be available")

    def testPersonCountAfterPlacingOnHut(self):
        self.assertEqual(0, self.board.person(self.redPlayer))
        self.assertEqual(0, self.board.personsOnHuts(self.redPlayer))
        self.board.placeOnHutIndex(0, self.redPlayer)
        self.assertEqual(1, self.board.person(self.redPlayer))
        self.assertEqual(1, self.board.personsOnHuts(self.redPlayer))

        self.assertEqual(0, self.board.person(self.bluePlayer))
        self.assertEqual(0, self.board.personsOnHuts(self.bluePlayer))        
        self.board.placeOnHutIndex(1, self.bluePlayer)
        self.assertEqual(1, self.board.person(self.bluePlayer))
        self.assertEqual(1, self.board.personsOnHuts(self.bluePlayer))  
        
    def testPlacePersonsWithoutResources(self):
        self.assertEqual(0, self.board.person(self.redPlayer))
        self.board.addHunters(2, self.redPlayer)
        self.board.addLumberjacks(2, self.redPlayer)

        self.assertEqual(4, self.board.person(self.redPlayer))

        self.board.addClayDiggers(1, self.redPlayer)
        
        self.assertEqual(5, self.board.person(self.redPlayer))
       
    def testIllegalPlacement(self):
        self.board.addStoneDiggers(2, self.redPlayer)
        
        self.assertEqual(2, self.board.person(self.redPlayer))
        from Board import PlacementError
        with self.assertRaises(PlacementError):
            self.board.addStoneDiggers(1, self.redPlayer)
        
        self.assertEqual(2, self.board.person(self.redPlayer))
        
    def testIsFinished(self):
        self.board = Board([SimpleHut(3,3,4), SimpleHut(3,3,4), SimpleHut(3,3,4), SimpleHut(3,3,4)])
        self.assertFalse(self.board.isFinished())
        self.board = Board([SimpleHut(3,3,4), SimpleHut(3,3,4), SimpleHut(3,3,4)])
        self.assertTrue(self.board.isFinished())
        
    def testReapResources(self):
        hutForRed = SimpleHut(3, 3, 4)
        hutForBlue = SimpleHut(3, 4, 4)
        self.board = Board([hutForRed, hutForBlue, SimpleHut(3,4,5), SimpleHut(4,5,6)])
        self.board.placeOnHut(hutForRed, self.redPlayer)
        self.board.placeOnHut(hutForBlue, self.bluePlayer)
        
        huts = self.board.reapResources(self.players)
        self.assertEqual(1, len(huts))
        self.assertEqual([hutForRed], huts)
        self.players.reverse()
        
        huts = self.board.reapResources(self.players)
        self.assertEqual([hutForBlue], huts)

    def testReapResourcesWithFarm(self):
        self.board.placeOnFarm(self.redPlayer)
        self.board.addClayDiggers(4, self.redPlayer)
        huts = self.board.reapResources(self.players)
        self.assertEqual(1, self.redPlayer.getFoodTrack())

def main():
#    suite = unittest.TestLoader().loadTestsFromTestCase(BoardTest)
#    unittest.TextTestRunner(verbosity=2).run(suite)

    # alternatively use this for shorter output
    unittest.main()

if __name__ == '__main__':
    main()
