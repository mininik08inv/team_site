from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Q
from datetime import datetime, timezone

from django.views.generic import ListView

from .models import Team, Player, Coach, Match, Achievement
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



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
        'title': 'Академия футбола Тамбов 2013'
    })


def achievements(request):
    achievements = Achievement.objects.all().order_by('-data_event')

    # Фильтрация по году
    year = request.GET.get('year')
    if year:
        achievements = achievements.filter(data_event__year=year).order_by('-data_event')

    # Фильтрация по городу
    city = request.GET.get('city')
    if city:
        achievements = achievements.filter(city=city).order_by('-data_event')

    # Фильтрация по названию турнира
    tournament_name = request.GET.get('tournament_name')
    if tournament_name:
        achievements = achievements.filter(tournament_name=tournament_name).order_by('-data_event')

    # Уникальные значения для фильтров
    cities = Achievement.objects.values_list('city', flat=True).distinct()
    tournaments = Achievement.objects.values_list('tournament_name', flat=True).distinct()

    # Статистика
    second_place = achievements.filter(final_place=2).count()
    victories = achievements.filter(final_place=1).count()
    third_place = achievements.filter(final_place=3).count()

    context = {
        'achievements': achievements,
        'cities': cities,
        'tournaments': tournaments,
        'second_place': second_place,
        'victories': victories,
        'third_place': third_place,
        'title': 'Достижения',
    }
    return render(request, 'team/achievements.html', context)


def achievement_detail(request, pk):
    achievement = get_object_or_404(Achievement, pk=pk)
    return render(request, 'team/achievement_detail.html', {'achievement': achievement, 'title': achievement.name, })


def player_detail(request, player_id):
    player = get_object_or_404(
        Player.objects.prefetch_related('goal_set__match'),
        id=player_id
    )
    main_photo = player.main_photo  # Основное фото игрока
    additional_photos = player.additional_photos.all()  # Дополнительные фото
    additional_videos = player.additional_videos.all()  # Видео игрока

    return render(request, 'team/player_detail.html', {
        'player': player,
        'main_photo': main_photo,
        'additional_photos': additional_photos,
        'additional_videos': additional_videos,
        'title': player.last_name,
    })

def coach_detail(request, coach_id):
    coach = get_object_or_404(Coach, id=coach_id)

    return render(request, 'team/coach_detail.html', {
        'coach': coach,
        'title': coach.last_name,
    })

class MatchListView(ListView):
    model = Match
    template_name = 'team/match_list.html'
    context_object_name = 'matches'
    paginate_by = 10
    ordering = ['-date']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Получение параметров фильтрации
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        status = self.request.GET.get('status')
        opponent = self.request.GET.get('opponent')

        # Фильтрация по датам
        if start_date or end_date:
            start_date = start_date or '2015-01-01'
            end_date = end_date or timezone.now().strftime('%Y-%m-%d')
            queryset = queryset.filter(date__range=[start_date, end_date])

        # Фильтрация по статусу и оппоненту
        if status:
            queryset = queryset.filter(status=status)
        if opponent:
            queryset = queryset.filter(second_team=opponent)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем отфильтрованный queryset
        queryset = self.get_queryset()

        # Агрегация данных
        context['total_matches'] = queryset.count()
        context['wins'] = queryset.filter(status='Победа').count()
        context['draws'] = queryset.filter(status='Ничья').count()
        context['defeats'] = queryset.filter(status='Поражение').count()
        context['total_goals_scored'] = queryset.aggregate(Sum('goals_scored'))['goals_scored__sum'] or 0
        context['total_goals_conceded'] = queryset.aggregate(Sum('goals_conceded'))['goals_conceded__sum'] or 0

        # Дополнительные данные для контекста
        context['opponents'] = Match.objects.values_list('second_team', flat=True).distinct()
        context['start_date'] = self.request.GET.get('start_date')
        context['end_date'] = self.request.GET.get('end_date')
        context['status'] = self.request.GET.get('status')
        context['opponent'] = self.request.GET.get('opponent')
        context['title'] = 'Прошедшие матчи'

        return context


def match_list(request):
    # Получение параметров фильтрации из GET-запроса
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status = request.GET.get('status')
    opponent = request.GET.get('opponent')

    # Базовый запрос
    matches = Match.objects.all().order_by('-date')

    # Фильтрация по датам
    if start_date or end_date:
        start_date = start_date or '2015-01-01'  # Значение по умолчанию, если start_date не указан
        end_date = end_date or datetime.now().strftime('%Y-%m-%d')  # Значение по умолчанию, если end_date не указан
        matches = matches.filter(date__range=[start_date, end_date])

    # Фильтрация по статусу и оппоненту
    if status:
        matches = matches.filter(status=status)
    if opponent:
        matches = matches.filter(second_team=opponent)

    # Агрегация данных
    total_matches = matches.count()
    wins = matches.filter(status='Победа').count()
    draws = matches.filter(status='Ничья').count()
    defeats = matches.filter(status='Поражение').count()
    total_goals_scored = matches.aggregate(Sum('goals_scored'))['goals_scored__sum'] or 0
    total_goals_conceded = matches.aggregate(Sum('goals_conceded'))['goals_conceded__sum'] or 0

    # Получение списка оппонентов
    opponents = Match.objects.values_list('second_team', flat=True).distinct()

    # Пагинация
    paginator = Paginator(matches, 10)  # 10 записей на страницу
    page_number = request.GET.get('page', 1)
    try:
        matches = paginator.page(page_number)
    except PageNotAnInteger:
        matches = paginator.page(1)
    except EmptyPage:
        matches = paginator.page(paginator.num_pages)

    # Контекст для шаблона
    context = {
        'matches': matches,
        'total_matches': total_matches,
        'wins': wins,
        'draws': draws,
        'defeats': defeats,
        'total_goals_scored': total_goals_scored,
        'total_goals_conceded': total_goals_conceded,
        'opponents': opponents,
        'start_date': start_date,
        'end_date': end_date,
        'status': status,
        'opponent': opponent,
        'title': 'Прошедшие матчи',
    }

    return render(request, 'team/match_list.html', context=context)


def match_detail(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    return render(request, 'team/match_detail.html',
                  {'match': match, 'title': match.first_team + '-' + match.second_team, })




def top_scorers(request):
    season_year = request.GET.get('season')

    # Базовый запрос
    queryset = Player.objects.all()

    # Если указан год, добавляем фильтр в аннотацию
    if season_year:
        try:
            year = int(season_year)
            queryset = queryset.annotate(
                goals=Sum(
                    'goal__goals',
                    filter=Q(goal__match__date__year=year)
                )
            ).filter(
                goals__gt=0
            )
        except ValueError:
            queryset = queryset.annotate(goals=Sum('goal__goals')).filter(goals__gt=0)
    else:
        queryset = queryset.annotate(goals=Sum('goal__goals')).filter(goals__gt=0)

    top_scorers = queryset.order_by('-goals')[:10]

    # Получаем список доступных годов
    current_year = datetime.now().year
    available_years = range(current_year, 2021, -1)  # От текущего года до 2020

    context = {
        'top_scorers': top_scorers,
        'available_years': available_years,
        'selected_season': season_year,
    }

    return render(request, 'team/top_scorers.html', context)