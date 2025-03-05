from django.shortcuts import render, get_object_or_404
from .models import Team, Player, Coach


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

    print(team_photos, team_videos)

    return render(request, 'team/team_detail.html', {
        'team': team,
        'players_by_position': players_by_position,
        'coaches': coaches,
        'team_photos': team_photos,
        'team_videos': team_videos,
    })


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
