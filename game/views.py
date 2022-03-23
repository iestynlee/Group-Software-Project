#What you need to render the html and files
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
#Need this here to set up path
sys.path.insert(0, '/Group-Software-Project')
from Player import *


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
	listlobbies = Lobby.objects.all()
	context = {'listlobbies': listlobbies}
	return render(request, "game/lobbies.html", context)

@login_required(login_url='game:login')
def inLobby(request, lobby_name):
	lobby = get_object_or_404(Lobby, pk=lobby_name)
	return render(request, 'game/lobby.html', {'lobby': lobby})

@login_required(login_url='game:login')
def addUser(request, lobby_name):
	lobby = Lobby.objects.get(pk=lobby_name)
	user = None
	if request.user.is_authenticated():
		username = request.user
		if lobby.is_occupied(username):
			lobby.users.add(username)
			return redirect('game:lobby')
		else: 
			return redirect('game:lobbies')
	else:
		return render(request, "users/error_page.html")
	
@login_required(login_url='game:login')
def cancelLobby(request, lobby_name):
	lobby = Lobby.objects.get(pk=lobby_name)
	lobby.delete()
	return redirect('game:lobbies')

@login_required(login_url='game:login')
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
def inGame(request):
	is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
	if is_ajax == True:
			location = [request.GET.get('longitude'), request.GET.get('latitude')]

			lon = location[0]
			lat = location[1]
			return JsonResponse({'lon': lon, 'lat':lat})

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
	player1 = Player(False, "NormalUser",[] ,True, names[:16])
	player2 = Player(False, "NormalUser2",[], True, names[16:])
	playerImposter = Player(True, "Imposter",[], True, [])
	return render(request, 'game/game.html',{'data':tasksLocation, 'names':names})
