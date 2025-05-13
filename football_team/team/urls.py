from django.urls import path
from . import views

urlpatterns = [
    path('', views.team_detail, name='team_detail'),
    path('player/<int:player_id>/', views.player_detail, name='player_detail'),
    path('matches/', views.match_list, name='match_list'),
    path('matches1/', views.MatchListView.as_view(), name='match_list1'),
    path('match_detail/<int:match_id>/', views.match_detail, name='match_detail'),
    path('achievements/', views.achievements, name='achievements'),
    path('achievement_detail/<int:pk>/', views.achievement_detail, name='achievement_detail'),
    path('top_scorers/', views.top_scorers, name='top_scorers'),

]