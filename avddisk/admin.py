from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'time_load')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'time_load')
    list_filter = ('name', 'time_load')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email')
    list_display_links = ('id', 'email')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('first_name', 'last_name', 'email')


admin.site.site_title = 'Админ-панель AvdDisk'
admin.site.site_header = 'Админ-панель AvdDisk'
admin.site.register(File, FileAdmin)
admin.site.register(Profile, ProfileAdmin)
