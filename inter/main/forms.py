from django import forms

class Adjastbasic(forms.Form):
    name=forms.CharField(strip=True, label='Имя устройства', min_length=2, max_length=10)
    speed=forms.IntegerField(min_value=1, label= 'Скорость, М/с')
    depth=forms.IntegerField(min_value=1, label='Глубинра, М')
    power=forms.IntegerField(min_value=1, label='Мощность, %')
    period=forms.IntegerField(min_value=1, label= 'Период работы, час')
    pause=forms.IntegerField(min_value=1, label= 'Время паузы, мин')
    periodInfo=forms.IntegerField(min_value=1, label= 'Период соединения, мин')

class Dateperiod(forms.Form):
    begin=forms.DateField(label='с', widget=forms.DateInput(attrs={'type':'date'}))
    end=forms.DateField(label='по', widget=forms.DateInput(attrs={'type':'date'}))