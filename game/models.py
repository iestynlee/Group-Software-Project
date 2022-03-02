from django.db import models

class Lobby(models.Model):
	lobby_code = models.CharField(max_length=18, unique=True)

	def players(self):
		return self.users.all()

#class Tasks(models.Model):
#	name = models.CharField(max_length=100)
#	location = models.PointField()