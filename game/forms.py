from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *

#Forms
class CreateUserForm(UserCreationForm):
	email = forms.EmailField(required=True, label='email',widget=forms.TextInput(attrs={'placeholder':'Email...'})) #Telling you that email is required
	username = forms.CharField(label='username',widget=forms.TextInput(attrs={'placeholder':'Username...'}))
	password1 = forms.CharField(label='password1',widget=forms.PasswordInput(attrs={'placeholder':'Password...'})) 
	password2 = forms.CharField(label='password2',widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password...'})) 

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2'] #This is the fields being used on the form

	#Function for saving the form
	def save(self, commit=True):
		user = super(CreateUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class LobbyForm(forms.ModelForm):
	class Meta:
		model = Lobby
		fields = ['lobby_name']
