from django.urls import path
from .import views

app_name = "Myaccount"
urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.profile_updates, name='profile_update'),
]