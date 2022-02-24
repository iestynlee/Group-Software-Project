from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

#Models
class CreateUserForm(UserCreationForm):
	email = forms.EmailField(required=True) #Telling you that email is required

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