from django.urls import path
from .views import * 

urlpatterns = [
    path('login/',     log_in,     name='log_in'),
    path('logout/',    log_out,    name='log_out'),
    path('register/',  register,  name='register'),
    
    path('profile_dashboard/', profile_dashboard, name='profile_dashboard'),
    path('profile/', profile, name='profile'),
]