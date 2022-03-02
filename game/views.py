#What you need to render the html and files
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory

#For the login and registeration system
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group

#GeoDjango
#from django.views import generic
#from django.contrib.gis.geos import fromstr
#from django.contrib.gis.db.models.functions import Distance
#from .models import Tasks

#Using the other functions on the other files
from .forms import CreateUserForm
from .utils import *

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

#The Game
@login_required(login_url='game:login')
def lobbies(request):
	return render(request, "game/lobbies.html")
