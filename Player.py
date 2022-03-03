from Task import Task


class Player:
   
    def __init__(self, isImposter, user, gpsLocation, isAlive, individualTasks):
        """
        Constructor function
        -----
        Parameters:
        isImposter - A boolean indicating whether the player is an imposter or not.
        user - The user assosiated with the player
        gpsLocation - the GPS location of the player
        isAlive -  a Boolean determining if the player is alive or dead.
        """
        self.isImposter = isImposter
        self.user = user
        self.gpsLocation = gpsLocation
        self.isAlive = isAlive
        self.individualTasks = []
        
        @property
        def isImposter(self):
            return self.__isImposter
        @isImposter.setter
        def isImposter(self, newImposter):
            self.__isImposter = newImposter

        @property
        def user(self):
            return self.user
        @user.setter
        def user(self, newUser):
            self.__user = newUser
        
        @property
        def gpsLocation(self):
            return self.__gpsLocation
        @gpsLocation.setter
        def gpsLocation(self, newGPSLocation):
            self.__gpsLocation = newGPSLocation
        
        @property
        def isAlive(self):
            return self.__isAlive
        @isAlive.setter
        def isAlive(self, newState):
            self.__isAlive = newState

        @property
        def individualTasks(self):
            return self.__individualTasks
        @individualTasks.setter
        def individualTasks(self, newIndividualTasks):
            self.__individualTasks = newIndividualTasks



    def doTask(self, task): 
        """
        This function allows the player to change the state of a task from pending to done, if the player
        is not an imposter 
        -----
        Paramaters:
        task - the task that will have its state to be changed
        -----
        Returns:
        The task that had its state changed

        """
        index = self.individualTasks.index(task)
        taskStateToBeChanged = self.individualTasks[index]
        if self.gpsLocation == taskStateToBeChanged.location:
            taskStateToBeChanged.isDone = True
            print("Task completed")
            return taskStateToBeChanged
    

    def killPlayer(self, player):
        """
        This function allows the player to change the state of a player from alive to dead, if the player
        is an imposter 
        -----
        Paramaters:
        player - the player to be killed have its state to be changed
        -----
        Returns:
        The player that has been killed
        """
        if self.gpsLocation == player.gpsLocation:
            if self.isAlive == True and self.isImposter == True:
                player.isAlive = False
        


