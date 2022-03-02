from django.urls import path, include
from . import views

from django.contrib.auth import views as auth_views

app_name='game'
urlpatterns = [
	#Home
	path('', views.home, name="home"),

	#Lobby
	path('lobbies/', views.lobbies, name="lobbies"),

	#Game


	#These are the urls for the registering and logging in for normal user
	path('register/', views.register, name="register"),
	path('login/', views.loginPage, name="login"),
	path('logout/', views.userLogout, name="logout"),

	#GameMaster Login
	path('login_gamemaster/', views.loginGamemaster, name="login_gamemaster"),

	#Password Reset
	path('password_reset/', auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"), name="password_reset"),
	path('password_reset_sent/', auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_sent.html"), name="password_reset_sent"),
	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_form.html"), name="password_reset_confirm"),
	path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_done.html"), name="password_reset_complete"),
]