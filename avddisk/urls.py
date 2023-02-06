from django.urls import path, re_path, include
from .views import *
from django.views.decorators.cache import cache_page
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

urlpatterns = [
    re_path(r'^$', start, name='home'),
    re_path(r'^registration$', RegisterUser.as_view(), name='registration'),
    re_path(r'^login$', LoginUser.as_view(), name="login"),
    re_path(r'^info$', ContactFormView.as_view(), name='info'),
    re_path(r'^user-page$', user_page, name='user_page'),
    re_path(r'^add-file$', AddFile.as_view(), name="addfile"),
    re_path(r'^file-list$', FileListView.as_view(), name='file'),
    re_path(r'^logout$', logout_user, name="logout"),
    path('dowload-file/<int:pk>', download_file, name='download_file'),
    path('delete-file/<int:pk>', delete_file, name='delete_file'),
    path('__debug__/', include('debug_toolbar.urls')),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('password-reset/', PasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='register/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='register/password_reset_complete.html'),
         name='password_reset_complete'),
]
