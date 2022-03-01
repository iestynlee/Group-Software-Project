class Player:
    
    
    def __init__(self, isImposter, user, gpsLocation, isAlive):
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
        pass

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
        pass



