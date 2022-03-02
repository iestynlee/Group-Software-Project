from enum import Enum
from operator import le
from queue import Empty
from time import sleep
from typing import List 
from Player import *
import random

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

        self.noOfPlayers = noOfPlayers
        self.state = state
        self.players = []
        self.tasks = []
        self.gameMaster = gameMaster
        
    @property
    def noOfPlayers(self):
        return self.__noOfPlayers
    @noOfPlayers.setter
    def noOfPlayers(self, newNoOfPlayers):
        self.__noOfPlayers = newNoOfPlayers
    
    @property
    def state(self):
        return self.__state
    @state.setter
    def state(self, newState):
        self.__state = newState

    @property
    def players(self):
        return self.__players
    @players.setter
    def players(self, newPlayers):
        self.__players = newPlayers

    @property
    def tasks(self):
        return self.__tasks
    @tasks.setter
    def tasks(self, newTasks):
        self.__tasks = newTasks
        
    @property
    def gameMaster(self):
        return self.__gameMaster
    @gameMaster.setter
    def gameMaster(self, newGameMaster):
        self.__gameMaster = newGameMaster
        

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
        
        print("Game is starting in 3")
        sleep(1)
        print("Game is starting in 2")
        sleep(1)
        print("Game is starting in 1")
        sleep(1)
        print("Game starting now")
        self.state = "IN_PROGRESS"

        while self.state == "IN_PROGRESS":
            if self.players.isAlive <= self.players.isAlive and self.players.isImposter:
                self.state == "FINISHED"

    
        

    def cancelGame(self) -> None:
        """
        This function is called when the Game Master clicks the cancel game button
        This function changes the state of the game to CANCELED and removes all players from the Game
        """
        self.state = "CANCELLED"
        print("Game master has cancelled the game")
        self.players.clear()

    def finishGame(self) -> None:
        """
        This function is called when a win condition of the game has been met.
        This function ends the game, changing the state to finished. 
        A message should be displayed depending on who won.
        """
        if self.players.isAlive <= self.players.isAlive and self.players.isImposter:
            print("Imposters Win")
        else:
            print("Crewmates win")
        

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
        self.players.append(user)
        print("Player " + user + " has joined the lobby")
        return user
        

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
        self.players.remove(user)
        print(user + " has been removed from the game")
        return user 

    def chooseImposter(self) -> List:
        """
        This function chooses an imposter(s) from the list of players in the games
        -----
        Returns:
        The player(s) chosen to be imposters in a list
        """
    
        numberOfImposters = input("Choose the desired number of imposters")
        listOfImposters = random.sample(self.players, numberOfImposters)
        return listOfImposters
        

    def distributeTasks(self) -> None:
        """
        This function takes all the tasks in the game and distibutes them evenly among 
        the non imposter players.
        """
        noOfIndividualTasks = len(self.tasks) % len(self.players)
        for i in range(len(self.players)):
            for x in range(noOfIndividualTasks):
                self.players[x].individualTask.append(random.choice(self.tasks))


    def addTasks(self, task):
        self.tasks.append(task)
