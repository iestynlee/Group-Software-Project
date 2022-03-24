from django.db import models
from django.contrib.auth.models import User, Group
import uuid

class Lobby(models.Model):
	lobby_name = models.CharField(max_length=200, default='Test', unique=True)
	users = models.ManyToManyField(User)
	#gameMaster = models.OneToOneField(User, on_delete=models.CASCADE)
	gameState = models.IntegerField(default=0)

	def __str__(self):
		return self.lobby_name
	def _users(self):
		return self.users.all()
	def _players(self):
		return self.player_set.all()
	def _is_occupied(self):
		return self.users.count() <= 11
	def _gameState(self):
		return self.gameState


class Player(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
	isImposter = models.BooleanField(default=False)
	isAlive = models.BooleanField(default=False)
	gpsLongitude = models.FloatField(default=0)
	gpsLatitude = models.FloatField(default=0)
	lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE, default=None)
	color = models.CharField(max_length=10, default="#000000")


	def __str__(self):
		return self.user.username
	def _user(self):
		return self.user
	def _isImposter(self):
		return self.isImposter
	def _isAlive(self):
		return self.isAlive
	def _gpsLongitude(self):
		return self.gpsLongitude
	def _gpsLatitude(self):
		return self.gpsLatitude
	def _color(self):
		return self.color

	def _taskList(self):
		return self.task_set.all()


class Task(models.Model):

	player = models.ForeignKey(Player, on_delete=models.CASCADE, default=None, blank=True, null=True)
	taskName =  models.CharField(max_length=200, default='Task')
	gpsLongitude = models.FloatField(default=0)
	gpsLatitude = models.FloatField(default=0)
	taskNumber = models.IntegerField(default=0)
	isDone = models.BooleanField(default=False)

	def __str__(self):
		return self.taskName
	def _player(self):
		return self.player
	def _gpsLongitude(self):
		return self.gpsLongitude
	def _gpsLatitude(self):
		return self.gpsLatitude
	def _taskNumber(self):
		return self.taskNumber
	def _isDone(self):
		return self.isDone
