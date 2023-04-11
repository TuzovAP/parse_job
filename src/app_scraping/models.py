from django.db import models

# create table "City" in db
from app_scraping.utils import from_cyrillic_to_eng


class City(models.Model):
    city_name = models.CharField(max_length=50,
                                 verbose_name='Название города',
                                 unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)  # blank - может быть пустым

    # корректирую написание админке
    class Meta:
        verbose_name = 'Название города'  # написание заголовка столбца
        verbose_name_plural = 'Название городов'  # написание таблицы в списке приложения

    # Переопределяю написание города в таблице
    def __str__(self):
        return self.city_name

    # Заполнение slug автоматом
    def save(self, *args, **kwargs):
        # заполняю slug, если он не указан
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.city_name))
        super().save(*args, **kwargs)



# Важно: тбл необходимо регестрировать в admin.py для отображение в админке на сайте
class LanguageProgramm(models.Model):
    language_name = models.CharField(max_length=50,
                                 verbose_name='Язык программирования',
                                 unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)  # blank - может быть пустым

    # корректирую написание админке
    class Meta:
        verbose_name = 'Язык программирования'  # написание заголовка столбца
        verbose_name_plural = 'Языки программирования'  # написание таблицы в списке приложения

    # Переопределяю написание в таблице
    def __str__(self):
        return self.language_name

    # Заполнение slug автоматом
    def save(self, *args, **kwargs):
        # заполняю slug, если он не указан
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.language_name))
        super().save(*args, **kwargs)


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Заголовок вакансии')
    salary = models.CharField(max_length=250, blank=True, verbose_name='Зарплата')
    company = models.CharField(max_length=250, verbose_name='Компания')
    description = models.TextField(verbose_name='Подробное описание вакансии')
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Название города')
    language = models.ForeignKey('LanguageProgramm', on_delete=models.CASCADE, verbose_name='Язык программирования')
    timestamp = models.DateField(auto_now_add=True)

    # корректирую написание админке
    class Meta:
        verbose_name = 'Описание вакансии'  # написание заголовка столбца
        verbose_name_plural = 'Описание вакансий'  # написание таблицы в списке приложения
        ordering = ['-timestamp']  # поле по которому произвожу сортировку

    # Переопределяю написание в таблице
    def __str__(self):
        return self.title


class Error(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    url = models.URLField(unique=False)
    er = models.CharField(max_length=250, verbose_name='Error')
