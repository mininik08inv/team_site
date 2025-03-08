from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from .models import Team, Player, Coach, Match, Achievement


def team_detail(request):
    team = Team.objects.first()  # Получаем первую команду
    if not team:
        return render(request, 'team/team_detail.html',
                      {'team': None, 'players_by_position': {}, 'coaches': [], 'team_photos': [], 'team_videos': []})

    # Группируем игроков по амплуа
    players_by_position = {
        'Вратари': team.players.filter(position='GK'),
        'Защитники': team.players.filter(position='DF'),
        'Полузащитники': team.players.filter(position='MF'),
        'Нападающие': team.players.filter(position='FW'),
    }
    coaches = team.coach_set.all()

    # Получаем все фото и видео команды
    team_photos = team.team_photo.all()  # Список всех фото команды
    team_videos = team.team_video.all()  # Список всех видео команды

    return render(request, 'team/team_detail.html', {
        'team': team,
        'players_by_position': players_by_position,
        'coaches': coaches,
        'team_photos': team_photos,
        'team_videos': team_videos,
    })


def achievements(request):
    achievements = Achievement.objects.all()
    victories = len(Achievement.objects.filter(final_place=1))
    second_place = len(Achievement.objects.filter(final_place=2))
    third_place = len(Achievement.objects.filter(final_place=3))
    return render(request, 'team/achievements.html', {'achievements': achievements,
                                                      'victories': victories, 'second_place': second_place,
                                                      'third_place': third_place})


def player_detail(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    main_photo = player.main_photo  # Основное фото игрока
    additional_photos = player.additional_photos.all()  # Дополнительные фото
    additional_videos = player.additional_videos.all()  # Видео игрока

    return render(request, 'team/player_detail.html', {
        'player': player,
        'main_photo': main_photo,
        'additional_photos': additional_photos,
        'additional_videos': additional_videos,
    })


def match_list(request):
    total_matches = Match.objects.all().count()
    wins = Match.objects.filter(status='Победа')
    draws = Match.objects.filter(status='Ничья')
    defeats = Match.objects.filter(status='Поражение')
    matches = Match.objects.all()
    total_goals_scored = Match.objects.aggregate(Sum('goals_scored'))['goals_scored__sum']
    total_goals_conceded = Match.objects.aggregate(Sum('goals_conceded'))['goals_conceded__sum']

    return render(request, 'team/match_list.html', {'matches': matches,
                                                    'total_matches': total_matches,
                                                    'wins': wins,
                                                    'draws': draws,
                                                    'defeats': defeats,
                                                    'total_goals_scored': total_goals_scored,
                                                    'total_goals_conceded': total_goals_conceded})
