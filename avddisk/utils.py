from .models import *
title = 'AvdBASE'

possibility = [{'title': "Личный кабинет", 'url_name': 'user_page'},
               {'title': "Загрузить файл", 'url_name': 'addfile'},
               {'title': "Список файлов", 'url_name': 'file'},
               {'title': "Обратная связь", 'url_name': 'info'},
               ]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['title'] = title
        context['files_uploaded'] = File.objects.all()
        context['possibility'] = possibility
        return context