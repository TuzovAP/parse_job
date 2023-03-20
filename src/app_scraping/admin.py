from django.contrib import admin
from .models import City, LanguageProgramm, Vacancy

# Register your models here.
admin.site.register(City)
admin.site.register(LanguageProgramm)
admin.site.register(Vacancy)
