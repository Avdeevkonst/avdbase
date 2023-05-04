from django.db import models
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    USERNAME_FIELD = 'first_name'
    first_name = models.CharField(max_length=15, verbose_name='Имя', default='', unique=True)
    last_name = models.CharField(max_length=15, verbose_name='Имя', default='')
    email = models.EmailField(max_length=30, verbose_name='Почта', default='')
    email_confirmed = models.BooleanField(default=False)
    time_registration = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации', blank=True, null=True)
    data_file = models.ForeignKey('File', on_delete=models.DO_NOTHING, verbose_name="Файл",
                                  default='', null=True, blank=True)

    class Meta:
        verbose_name = 'Зарегистрированные пользователи'
        verbose_name_plural = 'Зарегистрированные пользователи'
        ordering = ['first_name']

    def __str__(self):
        return self.first_name


class File(models.Model):
    name = models.FileField(upload_to='files/%Y/%m/', verbose_name='Загрузить файл', unique=True)
    time_load = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, default='', null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Загруженные файлы'
        verbose_name_plural = 'Загруженные файлы'
