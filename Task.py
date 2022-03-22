class Task:

    def __init__(self, name, number, latitude, longitude, isDone) -> None:
        """
        Constructor function
        -----
        Parameters:
        name - the name of the task
        location - the GPS location of the task
        isDone -  a boolean determining if the task is pending or done.
        """
        self.latitude = latitude
        self.longitude = longitude
        self.name = name
        self.number = number
        self.isDone = isDone

        @property
        def location(self):
            return self.__location
        @location.setter
        def location(self, newLocation):
            self.__location = newLocation

        @property
        def name(self):
            return self.__name
        @name.setter
        def name(self, newName):
            self.__name = newName

        @property
        def isDone(self):
            return self.__isDone
        @isDone.setter
        def isDone(self, newState):
            self.__isDone = newState