from django.db import models
from django.contrib.auth.models import User, Group
import uuid

class Lobby(models.Model):
	users = models.ManyToManyField(User)
	lobby_name = models.CharField(max_length=200, default='Test', unique=True)

	def __str__(self):
		return self.lobby_name

	def players(self):
		return self.users.all()

	def is_occupied(self):
		return self.users.count() >= 10