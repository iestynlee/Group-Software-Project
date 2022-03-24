from django.contrib.auth.models import Group

#This function is just used to check who is gamemaster or not
def is_gamemaster(user):
	return user.groups.filter(name='Gamemaster').exists()