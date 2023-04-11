from django.core.paginator import Paginator
from django.shortcuts import render

from .forms import FindJobForm
from .models import Vacancy

# Показываем для пользователя список всех вакансий в ДБ
def home_view_app_scrapping(request):
    # queryset всех вакансий в бд
    print(request.POST)
    print(request.GET)
    form_django = FindJobForm()
    return render(request, 'app_scraping/home.html', {'form_django': form_django})



def list_view_app_scrapping(request):
    # queryset всех вакансий в бд
    form_django = FindJobForm()
    city_name = request.GET.get('city')  # согласно переменной в form_django
    language_program = request.GET.get('language_program')
    context = {
        'city': city_name,
        'language_program': language_program,
        'form_django': form_django,
    }
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
    paginator = Paginator(qs, 5)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    context['vacancy_list'] = page_obj
    return render(request, 'app_scraping/list.html', context)  # ключи словаря могу использовать для отрисовки страницы
