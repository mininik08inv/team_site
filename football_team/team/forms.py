from django import forms

class MatchFilterForm(forms.Form):
    start_date = forms.DateField(label="Матчи с", required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label="до", required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    status = forms.ChoiceField(label="Статус", choices=[("", "Все"), ("Победа", "Победа"), ("Ничья", "Ничья"), ("Поражение", "Поражение")], required=False)
    opponent = forms.ChoiceField(label="Соперник", choices=[], required=False)

    def __init__(self, *args, **kwargs):
        opponents = kwargs.pop('opponents', [])
        super().__init__(*args, **kwargs)
        self.fields['opponent'].choices = [("", "Все")] + [(opp, opp) for opp in opponents]