import datetime
import os, sys
import django
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model



proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "parse_job.settings"

django.setup()
from app_scraping.models import Vacancy, Error
from parse_job.settings import EMAIL_HOST_USER

ADMIN_USER = EMAIL_HOST_USER
today = datetime.date.today()
subject = f"Рассылка вакансий за {today}"
text_content = f"Рассылка вакансий {today}"
from_email = EMAIL_HOST_USER
empty = '<h2>К сожалению на сегодня по Вашим предпочтениям данных нет. </h2>'

User = get_user_model()
qs = User.objects.filter(send_email=True).values('city', 'language_programm', 'send_message')
users_dct = {}
for i in qs:
    users_dct.setdefault((i['city'], i['language_programm']), [])
    users_dct[(i['city'], i['language_programm'])].append(i['send_message'])
if users_dct:
    params = {'city_id__in': [], 'language_programm_id__in': []}
    for pair in users_dct.keys():
        params['city_id__in'].append(pair[0])
        params['language_programm_id__in'].append(pair[1])
    # qs = Vacancy.objects.filter(**params).values()[:10]
    qs = Vacancy.objects.filter(**params, timestamp=today).values()
    vacancies = {}
    for i in qs:
        vacancies.setdefault((i['city_id'], i['language_programm_id']), [])
        vacancies[(i['city_id'], i['language_programm_id'])].append(i)
    for keys, emails in users_dct.items():
        rows = vacancies.get(keys, [])
        html = ''
        for row in rows:
            html += f'<h3"><a href="{ row["url"] }">{ row["title"] }</a></h3>'
            html += f'<p>{row["description"]} </p>'
            html += f'<p>{row["company"]} </p><br><hr>'
        _html = html if html else empty
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to]
            )
            msg.attach_alternative(_html, "text/html")
            msg.send()

qs = Error.objects.filter(timestamp=today)
subject = ''
text_content = ''
to = ADMIN_USER
_html = ''
if qs.exists():
    error = qs.first()
    data = error.data.get('errors', [])
    for i in data:
        _html += f'<p"><a href="{ i["url"] }">Error: { i["title"] }</a></p><br>'
    subject += f"Ошибки парсинга {today}"
    text_content += "Ошибки парсинга"
    data = error.data.get('user_data')
