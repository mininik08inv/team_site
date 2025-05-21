from django.contrib import admin
from django.utils.text import Truncator
from .models import Team, TeamPhoto, TeamVideo, Player, Coach, Photo, Video, Match, Goal, Achievement


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'data_event', 'tournament_name', )


@admin.register(TeamPhoto)
class TeamPhotoAdmin(admin.ModelAdmin):
    list_display = ('short_description', 'team')
    list_display_links = ('short_description', 'team')

    def short_description(self, obj):
        return Truncator(obj.description).chars(50)

    short_description.short_description = 'Описание фото'


@admin.register(TeamVideo)
class TeamVideoAdmin(admin.ModelAdmin):
    list_display = ('short_description', 'team')
    list_display_links = ('short_description', 'team')

    def short_description(self, obj):
        return Truncator(obj.description).chars(50)

    short_description.short_description = 'Описание видео'


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'position', 'in_the_team', 'last_modified')
    list_display_links = ('last_name', 'first_name')


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('short_description', 'player')
    list_display_links = ('short_description', 'player')

    def short_description(self, obj):
        return Truncator(obj.description).chars(30)

    short_description.short_description = 'Описание фото'


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('short_description', 'player')
    list_display_links = ('short_description', 'player')

    def short_description(self, obj):
        return Truncator(obj.description).chars(30)

    short_description.short_description = 'Описание видео'


@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name',)
    list_display_links = ('last_name', 'first_name')


# -------------matches-------------

class GoalInline(admin.TabularInline):
    model = Goal
    extra = 0

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    inlines = [GoalInline]
    list_display = ('__str__', 'status', 'date', 'city', 'tournament')
    ordering = ('date', 'status', )




@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('match', 'player', 'goals')
    list_display_links = ('match', 'player', 'goals')
