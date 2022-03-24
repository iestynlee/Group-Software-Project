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
		colors = ['black', 'blue', 'red', 'orange', 'light_green', 'yellow', 'pink', 'purple', 'light_blue', 'dark_green']
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
			ran1 = random.randint(0,len(players)-1)
			ran2 = random.randint(0,len(players)-1)

		else:
			numberOfImposters = 1
			ran1 = random.randint(0,len(players)-1)
		crewmates = []

		for i in range(0, len(players)):
			player = players[i]
			if i == ran1:
				player.isImposter = True
				player.save()
			else:
				player.isAlive
				player.save()
				crewmates.append(player)

		jsonFile = open("game/taskList.txt")
		tasksList = json.load(jsonFile)
		gameTasks = []
		#distribute tasks
		for x in tasksList["tasks"]:
			task = Task(taskName = x["name"], gpsLongitude = x["longitude"], gpsLatitude = x["latitude"], taskNumber =x["number"])
			task.save()
			gameTasks.append(task)
		jsonFile.close()
		noOfTasks = len(gameTasks)-1
		for i in crewmates:
			for j in range(4):
				num = random.randint(0,noOfTasks)
				print(num)
				task = gameTasks[num]
				task.player = i
				task.save()
				gameTasks.remove(task)

		url = '/game/' + lobby_name
		return redirect(url)
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
		if request.GET.get('longitude') != None:

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
			#wincondition check
			tasksAllFinished = True
			crewmatesAllDead = True
			crewmates = Player.objects.all().filter(lobby = thisLobby).filter(isImposter=False)
			for i in range(len(crewmates)):
				tasks = Task.objects.all().filter(player = i)
				for i in range(len(tasks)):
					if i.isDone == False:
						tasksAllFinished = False
				if i.isAlive == True:
					crewmatesAllDead = False
			#winconditioncheck end

			return JsonResponse({'otherPlayerData': otherPlayerData, 'tasksAllFinished':tasksAllFinished, 'crewmatesAllDead': crewmatesAllDead})
		elif request.GET.get('color'):
			#wincondition check
			player = Player.objects.all().filter(lobby = thisLobby).filter(color=request.Get.get('color'))
			deadPlayer = player[0]
			deadPlayer.isAlive = False
			deadPlayer.color = 'white'
			deadPlayer.save()
			crewmatesAllDead = True
			crewmates = Player.objects.all().filter(lobby = thisLobby).filter(isImposter=False)
			for i in range(len(crewmates)):
				if i.isAlive == True:
					crewmatesAllDead = False
			#winconditioncheck end
			return JsonResponse({'crewmatesAllDead':crewmatesAllDead})
		else:
			taskNum = request.GET.get('taskNumber')
			thisPlayer = Player.objects.get(user = request.user)
			thisTask = Task.objects.all().filter(player = thisPlayer).filter(taskNumber=taskNum)
			thisTask.isDone =True
			thisTask.save()
			tasksAllFinished = True
			crewmates = Player.objects.all().filter(lobby = thisLobby).filter(isImposter=False)
			for i in range(len(crewmates)):
				tasks = Task.objects.all().filter(player = i)
				for i in range(len(tasks)):
					if i.isDone == False:
						tasksAllFinished = False
			return JsonResponse({'tasksAllFinished':tasksAllFinished})

	taskLocation = []
	names = []
	locations=[]
	player = Player.objects.get(user = request.user)
	tasks = Task.objects.all().filter(player = player)
	#print("tasks " + str(tasks))
	for i in tasks:
		taskNum = i.taskNumber
		taskLon = i.gpsLongitude
		taskLat =i.gpsLatitude
		taskName = i.taskName
		names.append(taskName)
		taskLocation.append([taskNum, taskLon, taskLat])
	if player.isImposter == True:
		isImposter = 'true'
	else:
		isImposter = 'false'

	color = player.color

	return render(request, 'game/game.html',{'data':taskLocation, 'names':names, 'isImposter': isImposter, 'locations': locations, 'username':request.user, 'color': color})
