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