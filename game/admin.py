from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Lobby)
admin.site.register(Player)
admin.site.register(Task)