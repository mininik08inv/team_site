from django.db import models
from django.urls import reverse


class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название команды")
    description = models.TextField(verbose_name="Описание команды")
    matches_played = models.IntegerField(default=0, verbose_name="Сыграно матчей")
    matches_won = models.IntegerField(default=0, verbose_name="Победы")
    matches_drawn = models.IntegerField(default=0, verbose_name="Ничьи")
    matches_lost = models.IntegerField(default=0, verbose_name="Поражения")

    # photos = models.ManyToManyField('TeamPhoto', blank=True, related_name='teams')
    # videos = models.ManyToManyField('TeamVideo', blank=True, related_name='teams')

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"

    def __str__(self):
        return self.name

class Achievement(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название достижения")
    city = models.CharField(max_length=100, verbose_name="Город")
    data_event = models.DateField(verbose_name="Дата события")
    description = models.TextField(blank=True, null=True, verbose_name="Описание события")
    final_place = models.IntegerField(verbose_name="Итоговое место")
    tournament_name = models.CharField(max_length=200, verbose_name="Название турнира")
    participants_count = models.IntegerField(verbose_name="Количество участников")
    image = models.ImageField(upload_to='achievements/', blank=True, null=True, verbose_name="Изображение")

    class Meta:
        verbose_name = "Достижение"
        verbose_name_plural = "Достижения"


class TeamPhoto(models.Model):
    image = models.ImageField(upload_to='team_photos/', verbose_name="Фото команды")
    description = models.TextField(blank=True, null=True, verbose_name="Описание фото")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_photo', verbose_name="Команда")

    class Meta:
        verbose_name = "Командные фото"
        verbose_name_plural = "Командные фото"

    def __str__(self):
        return self.image.name


class TeamVideo(models.Model):
    video = models.FileField(upload_to='videos/', verbose_name="Командные видео")
    description = models.TextField(blank=True, null=True, verbose_name="Описание видео")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=1, related_name='team_video',
                             verbose_name="Команда")

    class Meta:
        verbose_name = "Командные видео"
        verbose_name_plural = "Командные видео"

    def __str__(self):
        return self.video.name


class Player(models.Model):
    POSITION_CHOICES = [
        ('GK', 'Вратарь'),
        ('DF', 'Защитник'),
        ('MF', 'Полузащитник'),
        ('FW', 'Нападающий'),
    ]

    IN_THE_TEAM_CHOICES = [
        ('YES', 'В составе'),
        ('NO', 'Не в составе'),
        ('UNKNOWN', 'Статус неопределен'),
    ]

    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    patronymic = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    date_of_birth = models.DateField(verbose_name="Дата рождения")
    main_photo = models.ImageField(upload_to='player_photos/', blank=True, verbose_name="Основное фото")
    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='players', verbose_name="Команда")
    position = models.CharField(max_length=2, choices=POSITION_CHOICES, verbose_name="Амплуа")
    in_the_team = models.CharField(max_length=10, choices=IN_THE_TEAM_CHOICES, default='YES', verbose_name="Статус")
    last_modified = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")

    class Meta:
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    def get_absolute_url(self):
        return reverse('player_detail', kwargs={'player_id': self.pk})


class Photo(models.Model):
    image = models.ImageField(upload_to='photos/', verbose_name="Фото")
    description = models.TextField(blank=True, null=True, verbose_name="Описание фото")
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='additional_photos', verbose_name="Игрок")

    class Meta:
        verbose_name = "Фото игроков"
        verbose_name_plural = "Фото игроков"

    def __str__(self):
        return self.image.name


class Video(models.Model):
    video = models.FileField(upload_to='videos/', verbose_name="Видео")
    description = models.TextField(blank=True, null=True, verbose_name="Описание видео")
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='additional_videos', verbose_name="Игрок")

    class Meta:
        verbose_name = "Видео игроков"
        verbose_name_plural = "Видео игроков"

    def __str__(self):
        return self.video.name


class Coach(models.Model):
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    patronymic = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    photo = models.ImageField(upload_to='coach_photos/', blank=True, verbose_name="Фото тренера")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    start_of_coaching_career = models.DateField(blank=True, null=True,
                                                verbose_name="Дата начала тренерской деятельности")
    team = models.ForeignKey('Team', on_delete=models.CASCADE, verbose_name="Команда")

    class Meta:
        verbose_name = "Тренер"
        verbose_name_plural = "Тренеры"

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'


# -------------------matches----------------------------------

class Match(models.Model):
    STAGE_CHOICES = [
        ('1 тур', '1 тур'),
        ('2 тур', '2 тур'),
        ('3 тур', '3 тур'),
        ('4 тур', '4 тур'),
        ('1/8', '1/8'),
        ('1/4', '1/4'),
        ('Полуфинал', 'Полуфинал'),
        ('Финал', 'Финал'),
        ]

    STATUS_CHOICES = [
        ('Победа', 'Победа'),
        ('Ничья', 'Ничья'),
        ('Поражение', 'Поражение'),
    ]

    first_team = models.CharField(max_length=100, default="Синие", verbose_name="Первая команда")
    second_team = models.CharField(max_length=100, default="Команда 2", verbose_name="Вторая команда")
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, verbose_name="Статус игры")
    # result = models.CharField(max_length=20, blank=True, null=True, verbose_name="Результат")
    goals_scored = models.IntegerField(default=0, verbose_name="Забитые мячи")
    goals_conceded = models.IntegerField(default=0, verbose_name="Пропущенные мячи")
    date = models.DateField(verbose_name="Дата")
    city = models.CharField(max_length=100, verbose_name="Город")
    tournament = models.CharField(max_length=100, verbose_name="Турнир")
    stage = models.CharField(max_length=100, choices=STAGE_CHOICES, default='Первый круг', verbose_name="Стадия турнира")
    description = models.TextField(blank=True, verbose_name="Описание матча")
    players = models.ManyToManyField('Player', through='Goal')


    class Meta:
        verbose_name = "Матч"
        verbose_name_plural = "Матчи"

    def __str__(self):
        commands = self.first_team + ' - ' + self.second_team
        return commands

    def get_absolute_url(self):
        return reverse('match_detail', kwargs={'match_id': self.pk})


class Goal(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, verbose_name='Матч')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='Игрок')
    goals = models.IntegerField()

    class Meta:
        verbose_name = "Гол игрока"
        verbose_name_plural = "Голы игрока"


# class PhotoOfMatch(models.Model):
#     album = models.ForeignKey('PhotoAlbum', related_name='photos', on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='photosOfMatch/', verbose_name="Фото матча")
#     description = models.TextField(blank=True, null=True, verbose_name="Описание")
#
#     class Meta:
#         verbose_name = "Фото матча"
#         verbose_name_plural = "Фотографии матчей"
#
#
#
#
# class VideoOfMatch(models.Model):
#     album = models.ForeignKey('VideoAlbum', related_name='videos', on_delete=models.CASCADE)
#     video = models.FileField(upload_to='videosOfMatch/', verbose_name="Видео матча")
#     description = models.TextField(blank=True, null=True)
#
#     class Meta:
#         verbose_name = "Видео матча"
#         verbose_name_plural = "Видео матчей"
#
#
# class PhotoAlbum(models.Model):
#     match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='photo_album')
#     name = models.CharField(max_length=100, verbose_name="Название альбома")
#     description = models.TextField(blank=True, null=True, verbose_name="Описание альбома")
#
#     class Meta:
#         verbose_name = "Фотоальбом матча"
#         verbose_name_plural = "Фотоальбомы матчей"
#
#     def __str__(self):
#         return self.name
#
#     def get_absolute_url(self):
#         return reverse('photo_album_detail', kwargs={'photo_album_id': self.pk})
#
#
# class VideoAlbum(models.Model):
#     match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='video_album')
#     name = models.CharField(max_length=100, verbose_name="Название альбома")
#     description = models.TextField(blank=True, null=True, verbose_name="Описание альбома")
#
#     class Meta:
#         verbose_name = "Видеоальбом матча"
#         verbose_name_plural = "Видеоальбомы матчей"
