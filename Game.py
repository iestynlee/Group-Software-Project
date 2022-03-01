from enum import Enum
from typing import List 
from Player import *

class State(Enum):
    PENDING = 1
    IN_PROGRESS = 2
    FINISHED = 3
    CANCELED = 4

class Game:

    def __init__(self, noOfPlayers, state, players, tasks, gameMaster) -> None:
        """
        Constructor function
        -----
        Paramaters:
        noOfPlayers - the number of players currently in the game
        state - the state of the game
        players - A list of the players included in the game
        tasks - 
        gameMaster - the Game Master of the Game
        """
        pass

    def startGame(self) -> None:
        """
        This function will be called when the Game Master clicks start game from the game lobby

        This functions sets up and starts the game, and then continuously checks for win conditions.
        (This could be done with threading).
        The win conditions are: 
        All tasks asigned to players are done 
        OR 
        The number of imposters is equal or more to the number of crewmates
        """
        pass

    def cancelGame(self) -> None:
        """
        This function is called when the Game Master clicks the cancel game button

        This function changes the state of the game to CANCELED and removes all players from the Game
        """
        pass

    def finishGame(self) -> None:
        """
        This function is called when a win condition of the game has been met.

        This function ends the game, changing the state to finished. 
        A message should be displayed depending on who won.
        """
        pass

    def addPlayer(self, user) -> Player:
        """
        This function is called when a user joins the game's lobby.

        This function creates a player associated with the user and adds it to the game.
        -----
        Paramaters:
        user - The user who joined the lobby
        -----
        Returns:
        The player added to the game
        """
        pass

    def removePlayer(self, user) -> Player:
        """
        This function is called when a user leaves the game's lobby.

        This function removes a player from the game's lobby
        -----
        Paramaters:
        user - The user who left the lobby
        -----
        Returns:
        The player removed from the game
        """
        pass

    def chooseImposter(self) -> List:
        """
        This function chooses an imposter(s) from the list of players in the games
        -----
        Returns:
        The player(s) chosen to be imposters in a list
        """
        pass

    def distributeTasks(self) -> None:
        """
        This function takes all the tasks in the game and distibutes them evenly among 
        the non imposter players.
        """
        pass
    
    