from django.db import models
from django.contrib.auth.models import User, Group
import uuid

class Lobby(models.Model):
	users = models.ManyToManyField(User)
	lobby_code = models.UUIDField(default=uuid.uuid4, editable=False)
	#lobby_code = models.CharField(max_length=18, unique=True)

	def players(self):
		return self.users.all()

	def is_occupied(self):
		return self.users.count() >= 10