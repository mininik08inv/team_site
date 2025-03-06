from django.urls import path
from . import views

urlpatterns = [
    path('', views.team_detail, name='team_detail'),
    path('player/<int:player_id>/', views.player_detail, name='player_detail'),
    path('matches/', views.match_list, name='match_list'),
    path('achievements/', views.achievements, name='achievements'),
]