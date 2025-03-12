from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from datetime import datetime
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
    victories = len(achievements.filter(final_place=1))
    second_place = len(achievements.filter(final_place=2))
    third_place = len(achievements.filter(final_place=3))
    return render(request, 'team/achievements.html', {'achievements': achievements,
                                                      'victories': victories, 'second_place': second_place,
                                                      'third_place': third_place})


def achievement_list(request):
    achievements = Achievement.objects.all()
    return render(request, 'achievements/achievement_list.html', {'achievements': achievements})


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
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status = request.GET.get('status')
    opponent = request.GET.get('opponent')

    matches = Match.objects.all().order_by('-date')

    # Фильтрация по датам
    if start_date or end_date:
        start_date = start_date or '2015-01-01'
        end_date = end_date or datetime.now().strftime('%Y-%m-%d')
        matches = matches.filter(date__range=[start_date, end_date]).order_by('-date')

    # Фильтрация по статусу и оппоненту
    if status:
        matches = matches.filter(status=status).order_by('-date')
    if opponent:
        matches = matches.filter(second_team=opponent).order_by('-date')

    # Агрегация данных
    total_matches = matches.count()
    wins = matches.filter(status='Победа').count()
    draws = matches.filter(status='Ничья').count()
    defeats = matches.filter(status='Поражение').count()
    total_goals_scored = matches.aggregate(Sum('goals_scored'))['goals_scored__sum'] or 0
    total_goals_conceded = matches.aggregate(Sum('goals_conceded'))['goals_conceded__sum'] or 0

    # Получение списка оппонентов
    opponents = Match.objects.values_list('second_team', flat=True).distinct()

    context = {
        'matches': matches,
        'total_matches': total_matches,
        'wins': wins,
        'draws': draws,
        'defeats': defeats,
        'total_goals_scored': total_goals_scored,
        'total_goals_conceded': total_goals_conceded,
        'opponents': opponents,
    }

    return render(request, 'team/match_list.html', context=context)


def match_detail(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    return render(request, 'team/match_detail.html', {'match': match})


def top_scorers(request):
    # Получаем список из 10 лучших бомбардиров
    top_scorers = Player.objects.annotate(goals=Sum('goal__goals')).filter(goals__gt=0).order_by('-goals')[:10]
    print(top_scorers)
    return render(request, 'team/top_scorers.html', {'top_scorers': top_scorers})
