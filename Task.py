class Task:

    def __init__(self, name, location, isDone) -> None:
        """
        Constructor function
        -----
        Parameters:
        name - the name of the task
        location - the GPS location of the task
        isDone -  a boolean determining if the task is pending or done.
        """
        self.location = location
        self.name = name
        self.isDone = isDone

        @property
        def location(self):
            return self.location
        @location.setter
        def location(self, newLocation):
            self.location = newLocation

        @property
        def name(self):
            return self.name
        @name.setter
        def name(self, newName):
            self.name = newName
        
        @property
        def isDone(self):
            return self.isDone
        @isDone.setter
        def isDone(self, newState):
            self.isDone = newState
