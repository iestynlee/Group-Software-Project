from django.urls import path, include
from . import views

from django.contrib.auth import views as auth_views

app_name='users'
urlpatterns = [
	path('', views.home, name="home"),

	#These are the urls for the registering and logging in
	path('register/', views.register, name="register"),
	path('login/', views.loginPage, name="login"),
	path('logout/', views.userLogout, name="logout"),

	#Password Reset
	path('password_reset/', auth_views.PasswordResetView.as_view(), name="password_reset"),
	path('password_reset_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_sent"),
	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
	path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name= "password_reset_complete"),
]