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

import json


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
def add_user_to_lobby(request, lobby_name):
	lobby = Property.objects.get(Lobby, lobby_name)
	if lobby.users.filter(pk=request.user.pk).exists():
		return redirect('game:lobby')
	elif not lobby.is_occupied(request.user):
		lobby.users.add(request.user)
		return redirect('game:lobby')
	else:
		return render(request, "users/error_page.html")

@login_required(login_url='game:login')
def cancelLobby(request):
	cancel = lobby.objects.filter(id=id)
	cancel.delete()

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
	jsonFile = open("game/taskList.txt")
	tasksList = json.load(jsonFile)
	tasksLocation=[]
	for x in tasksList["tasks"]:
		anInstance = [x["latitude"], x["longitude"]]
		tasksLocation.append(anInstance)
	jsonFile.close()
	return render(request, 'game/game.html',{'data':tasksLocation})
