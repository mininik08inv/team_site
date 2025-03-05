from django.contrib import admin
from django.utils.text import Truncator
from .models import Team, TeamPhoto, TeamVideo, Player, Coach, Photo, Video


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(TeamPhoto)
class TeamPhotoAdmin(admin.ModelAdmin):
    list_display = ('short_description',)

    def short_description(self, obj):
        return Truncator(obj.description).chars(50)

    short_description.short_description = 'Описание фото'


@admin.register(TeamVideo)
class TeamVideoAdmin(admin.ModelAdmin):
    list_display = ('short_description',)

    def short_description(self, obj):
        return Truncator(obj.description).chars(50)

    short_description.short_description = 'Описание видео'


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'position', 'last_modified')
    list_display_links = ('last_name', 'first_name')


@admin.register(Photo)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('short_description', 'player')

    def short_description(self, obj):
        return Truncator(obj.description).chars(30)

    short_description.short_description = 'Описание фото'


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('short_description', 'player')

    def short_description(self, obj):
        return Truncator(obj.description).chars(30)

    short_description.short_description = 'Описание видео'


@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name',)
    list_display_links = ('last_name', 'first_name')
