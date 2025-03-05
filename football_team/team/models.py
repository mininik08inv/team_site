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
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=1, related_name='team_video', verbose_name="Команда")

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

    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    patronymic = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    date_of_birth = models.DateField(verbose_name="Дата рождения")
    main_photo = models.ImageField(upload_to='player_photos/', blank=True, verbose_name="Основное фото")
    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='players', verbose_name="Команда")
    position = models.CharField(max_length=2, choices=POSITION_CHOICES, verbose_name="Амплуа")
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
