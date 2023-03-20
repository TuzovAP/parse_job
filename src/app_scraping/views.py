from django.shortcuts import render

from .forms import FindJobForm
from .models import Vacancy

# Показываем для пользователя список всех вакансий в ДБ
def home_view_app_scrapping(request):
    # queryset всех вакансий в бд
    print(request.POST)
    print(request.GET)
    form_django = FindJobForm()
    city_name = request.GET.get('city')  # согласно переменной в form_django
    language_program = request.GET.get('language_program')
    qs = []
    _filter = {}
    if city_name:
        print(city_name)
        _filter['city__slug'] = city_name.lower()  # связь тбл Vacancy и City ('city__city_name')
    if language_program:
        print(language_program)
        _filter['language__slug'] = language_program.lower()  # связь тбл Vacancy и LanguageProgramm ('language__language_name')
    print(_filter)
    # qs = Vacancy.objects.all()  # all record in db
    qs = Vacancy.objects.filter(**_filter)  # all record in db
    return render(request, 'app_scraping/home.html', {'vacancy_list': qs,
                                                      'form_django': form_django})
