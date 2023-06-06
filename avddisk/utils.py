from .models import *

title = 'AvdDisk'

possibility = [{'title': "Личный кабинет", 'url_name': 'user_page'},
               {'title': "Загрузить файл", 'url_name': 'addfile'},
               {'title': "Список файлов", 'url_name': 'file'},
               {'title': "Обратная связь", 'url_name': 'info'},
               {'title': "Новости", 'url_name': 'news'},
               {'title': "Погода", 'url_name': 'weather'},
               ]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['title'] = title
        context['files_uploaded'] = File.objects.all()
        context['possibility'] = possibility
        return context
