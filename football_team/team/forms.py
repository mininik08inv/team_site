from django import forms
from .models import Team, Player
from .fields import MultipleFileField

class TeamForm(forms.ModelForm):
    photos = MultipleFileField(required=False)  # Поле для загрузки фото команды
    videos = MultipleFileField(required=False)  # Поле для загрузки видео команды

    class Meta:
        model = Team
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        photos = self.cleaned_data.get('photos', [])
        videos = self.cleaned_data.get('videos', [])
        if photos:
            instance.photos = photos  # Сохраняем файлы
        if videos:
            instance.videos = videos  # Сохраняем файлы
        if commit:
            instance.save()
        return instance

class PlayerForm(forms.ModelForm):
    photos = MultipleFileField(required=False)  # Поле для загрузки фото игрока
    videos = MultipleFileField(required=False)  # Поле для загрузки видео игрока

    class Meta:
        model = Player
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        photos = self.cleaned_data.get('photos', [])
        videos = self.cleaned_data.get('videos', [])
        if photos:
            instance.photos = photos  # Сохраняем файлы
        if videos:
            instance.videos = videos  # Сохраняем файлы
        if commit:
            instance.save()
        return instance
