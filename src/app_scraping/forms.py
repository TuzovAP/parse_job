from django import forms
from app_scraping.models import City, LanguageProgramm


class FindJobForm(forms.Form):
    # выпадающий список городов
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),  # получаю все города из тбл
        to_field_name='slug',  # к какому полю обращаться в тбл
        required=False,  # может быть пустым
        # добавляю название класса для отрисовки через bootstrap
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Город',  # отрисовка на странице
    )
    language_program = forms.ModelChoiceField(queryset=LanguageProgramm.objects.all(),
                                              to_field_name='slug',
                                              required=False,  # может быть пустым
                                              widget=forms.Select(attrs={'class': 'form-control'}),
                                              label='Язык программирования',  # отрисовка на странице

                                              )

