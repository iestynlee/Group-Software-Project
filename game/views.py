#What you need to render the html and files
from turtle import color
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.forms import inlineformset_factory

#For the login and registeration system
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group

from django.template import loader
from django.http import Http404
from django.http import JsonResponse

import json
import sys
import random



#GeoDjango
#from django.views import generic
#from django.contrib.gis.geos import fromstr
#from django.contrib.gis.db.models.functions import Distance
#from .models import Tasks

#Using the other functions from the other files
from .forms import *
from .utils import *
from .models import *

#Registration & Login
def register(request):
	#If you are logged in already it will send you to the home
	if request.user.is_authenticated:
		return redirect('game:home')
	else:
		if request.method == 'POST':
			form = CreateUserForm(request.POST) #Creates the form using the forms.py
			if form.is_valid():
				user = form.save() #Saves the form
				messages.info(request, "Registration Successful")
				return redirect('game:login') #Redirects you to login after registration is successful

			messages.error(request, "Unsuccessful Registration. Invalid information") #This is when it doesn't have the requirements it asks
		form = CreateUserForm() #For making the form
	context = {'form':form}
	return render(request, 'users/register.html', context)

def loginPage(request):
	#If you are logged in already it will send you to the home
	if request.user.is_authenticated:
		return('game:home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username') #Asks for username
			password = request.POST.get('password') #Asks for password
			#This authenicates and checks the username and password
			user = authenticate(request, username=username, password=password)
			#If the user is incorrect it won't run this
			if is_gamemaster(user) == False:
				if user is not None:
					login(request, user)
					return redirect('game:home') #Redirects to home
				else:
					messages.info(request, 'Username or Password is incorrect')
			else:
				messages.info(request, 'This account is a Gamemaster, Go to the Gamemaster Login')

	context = {}
	return render(request, 'users/login.html', context)

def loginGamemaster(request):
	#If you are logged in already it will send you to the home
	if request.user.is_authenticated:
		return('game:home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username') #Asks for username
			password = request.POST.get('password') #Asks for password
			#This authenicates and checks the username and password
			user = authenticate(request, username=username, password=password)
			#If the user is incorrect it won't run this
			if is_gamemaster(user) == True:
				if user is not None:
					login(request, user)
					return redirect('game:home') #Redirects to home
				else:
					messages.info(request, 'Username or Password is incorrect')
			else:
				messages.info(request, 'Your Account is not a Gamemaster')

	context = {}
	return render(request, 'users/login_gamemaster.html', context)

def userLogout(request):
	logout(request) #Simple logout request sends you back to login
	return redirect('game:login')

@login_required(login_url='game:login') #This is used to tell the webapp that you can't access the homepage without logging in
def home(request):
	return render(request, "users/home.html")

#Lobby
@login_required(login_url='game:login')
def lobbies(request):
	Player.objects.filter(user = request.user).delete
	listlobbies = Lobby.objects.all().filter(gameState = 0)
	context = {'listlobbies': listlobbies}
	return render(request, "game/lobbies.html", context)

@login_required(login_url='game:login')
def inLobby(request, lobby_name):
	thislobby = get_object_or_404(Lobby, pk=lobby_name)
	if request.method=='POST':
		thislobby.gameState=1
		thislobby.save()
		users = thislobby._users()
		colors = ['#000000', '#0000FF', '#FF0000', '#FFA500', '#90EE90', '#FFFF00', '#FFC0CB', '#6a0dad', '#ADD8E6', '#006400']
		#players created
		print("The length of users " + str(len(users)))
		for i in range(len(users)):
			player = Player(user = users[i], lobby = thislobby, color = colors[i])
			player.save()
		#decide imposters
		players = Player.objects.all().filter(lobby = thislobby)
		print("THe players" + str(players))
		ran1 = -1
		ran2 = -1
		if len(players) >=7:
			numberOfImposters = 2
			ran1 = random.randint(0,len(players))
			ran2 = random.randint(0,len(players))

		else:
			numberOfImposters = 1
			ran1 = random.randint(0,len(players))

		for i in range(0, len(players)):
			if i == ran1:
				player = players[i]
				player.isImposter = True
				player.save()
		jsonFile = open("game/taskList.txt")
		tasksList = json.load(jsonFile)
		gameTasks = []
		crewmates = []
		for x in players:
			if x._isImposter() == False:
				crewmates.append(player)
		#distribute tasks
		for x in tasksList["tasks"]:
			task = Task(taskName = x["name"], gpsLongitude = x["longitude"], gpsLatitude = x["latitude"], taskNumber =x["number"])
			task.save()
			gameTasks.append(task)
		jsonFile.close()
		noOfTasks = len(gameTasks)
		for i in crewmates:
			nums = random.sample(range(noOfTasks-1), 4)
			for j in range(4):
				task = gameTasks[nums[j]]
				task.player = i
				task.save()
				gameTasks.remove(task)
		return render(request, 'game/lobby.html', {'lobby': thislobby})
	else:
		username = request.user
		if thislobby._is_occupied() and thislobby.gameState==0:
			thislobby.users.add(username)
			thislobby.save()
			print(str(thislobby.users))
			return render(request, 'game/lobby.html', {'lobby': thislobby, 'users':thislobby._users})
		else:
			return redirect('game:lobbies')

@login_required(login_url='game:login')
def addUser(request, lobby_name):
	lobby = Lobby.objects.get(pk=lobby_name)
	username = request.user
	print("username" + username)
	if lobby.is_occupied():
		lobby.users.add(username)
		lobby.save()
		return redirect('game:lobby')
	else:
		return redirect('game:lobbies')


@login_required(login_url='game:login')
def cancelLobby(request, lobby_name):
	lobby = Lobby.objects.get(pk=lobby_name)
	lobby.delete()
	return redirect('game:lobbies')

@login_required (login_url='game:login')
def lobbyForm(request):
	form = LobbyForm()
	if request.method == 'POST':
		form = LobbyForm(request.POST)
		if form.is_valid():
			form.save()
			redirect('game:lobbies')
	return render(request,"game/createLobby.html",{'form':form})


#The Game
@login_required(login_url='game:login')
def inGame(request, lobby_name):
	thisLobby = Lobby.objects.get(pk=lobby_name)
	is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
	if is_ajax == True:
			location = [request.GET.get('longitude'), request.GET.get('latitude')]
			thisPlayer = Player.objects.get(user = request.user)
			thisPlayer.gpsLongitude = location[0]
			thisPlayer.gpsLatitude = location[1]
			otherPlayers = Player.objects.all().filter(lobby = thisLobby).exclude(user = request.user)
			otherPlayerData = []
			for i in range(len(otherPlayers)):
				playerData = []
				anotherPlayer = otherPlayers[i]
				playerData.append(anotherPlayer.gpsLongitude)
				playerData.append(anotherPlayer.gpsLatitude)
				playerData.append(anotherPlayer.color)
				otherPlayerData.append(playerData)
			return JsonResponse({'otherPlayerData': otherPlayerData})

	jsonFile = open("game/taskList.txt")
	tasksList = json.load(jsonFile)
	tasksLocation=[]
	names=[]
	for x in tasksList["tasks"]:
		anInstance = [x["latitude"], x["longitude"], x["number"]]
		tasksLocation.append(anInstance)
		names.append(x["name"])
	jsonFile.close()
	#Example of game
	isImposter = 'false'
	locations = [[50.73773205777886, -3.5273476951213922], [50.737420204728565, -3.5390163992138413]]

	return render(request, 'game/game.html',{'data':tasksLocation, 'names':names, 'isImposter': isImposter, 'locations': locations})
