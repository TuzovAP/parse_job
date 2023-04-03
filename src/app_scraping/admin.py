from django.contrib import admin
from .models import City, LanguageProgramm, Vacancy, Error

# Register your models here.
admin.site.register(City)
admin.site.register(LanguageProgramm)
admin.site.register(Vacancy)
admin.site.register(Error)
