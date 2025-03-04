from django.urls import path
from . import views

urlpatterns = [
    path('', views.team_detail, name='team_detail'),
    path('player/<int:player_id>/', views.player_detail, name='player_detail'),
]