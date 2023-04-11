import codecs
import os, sys
from django.contrib.auth import get_user_model


path_abs = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(path_abs)
os.environ["DJANGO_SETTINGS_MODULE"] = "parse_job.settings"

import django
django.setup()


from app_scraping.hh_parse import parse_hh
from app_scraping.rabota_parse import parse_rabota
from app_scraping.models import Vacancy, City, LanguageProgramm, Error


User = get_user_model()

def get_setting_user():
    q_dict = User.objects.filter(send_message=True).values()  # .values() позволяет получить словарь. Без него возвращается qs
    setting_set = set((q['city_id'], q['language_programm_id']) for q in q_dict)
    return setting_set

q = get_setting_user()

# из таблицы City забираю город СПб
city = City.objects.filter(city_name='Санкт-Петербург').first()
print(city)
# собираю ваканскии с hh
url_hh = 'https://spb.hh.ru/search/vacancy?search_field=name&search_field=company_name&search_field=description&enable_snippets=false&text=Python&from=suggest_post'
vacancy_list_hh, er_hh = parse_hh(url=url_hh)
# собираю ваканскии с rabota
url_rabota = 'https://spb.rabota.ru/?query=python&sort=relevance&all_regions=1'
vacancy_list_rabota, er_rabota = parse_rabota(url=url_rabota)

# сохраняю результат в БД
for job in vacancy_list_hh:
    vacancy = Vacancy(
        url=job['link'],
        title=job['title'],
        salary=job['salary'],
        company=job['company'],
        city=City.objects.filter(city_name=job['city']).first(),
        language=LanguageProgramm.objects.filter(language_name='Python').first(),
    )
    try:
        vacancy.save()
    except django.db.utils.IntegrityError as ex:
        print(f'Er save job: {job}, er: {ex}')
        er = Error(
            url=job['link'],
            er=ex,
        ).save()
        pass

for job in vacancy_list_rabota:
    vacancy = Vacancy(
        url=job['link'],
        title=job['title'],
        salary=job['salary'],
        company=job['company'],
        city=City.objects.filter(city_name=job['city']).first(),
        language=LanguageProgramm.objects.filter(language_name='Python').first(),
    )
    try:
        vacancy.save()
    except django.db.utils.IntegrityError as ex:
        print(f'Er save job: {job}, er: {ex}')
        er = Error(
            url=job['link'],
            er=ex,
        ).save()
        pass




