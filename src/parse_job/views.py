import datetime

from django.shortcuts import render


def home(request):
    data = datetime.datetime.now()
    name = 'Sasha'
    django_dict = {'data': data, 'name': name}
    return render(request, 'base.html', context=django_dict)
