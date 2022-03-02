from django.contrib.auth.models import Group

def is_gamemaster(user):
	return user.groups.filter(name='Gamemaster').exists()