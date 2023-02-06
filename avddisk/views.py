from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponseNotFound, HttpResponse, Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View, generic
from django.views.generic import ListView, CreateView, FormView
from avddisk.forms import *
from avddisk.token import account_activation_token
from avddisk.utils import *
from avdbase.settings import *
import mimetypes
import os


def download_file(request, pk):
    filename = File.objects.get(pk=pk)
    filepath = filename.name.path
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


def delete_file(request, pk):
    if request.method == 'POST':
        file = File.objects.get(pk=pk)
        file.delete()
    return redirect('file')




def start(request):
    context = {'title': title,
               'possibility': possibility}
    return render(request, 'base/index.html', context=context)


@login_required
def user_page(request):
    context = {'title': title,
               'possibility': possibility}
    return render(request, 'base/user_page.html', context=context)


class AddFile(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddFileForm
    template_name = 'base/addfile.html'
    success_url = reverse_lazy('file')
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(**kwargs)
        return dict(list(context.items()) + list(c_def.items()))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.author = request.user
            file.save()
            return redirect('file')
        else:
            form = AddFileForm()
        return render(request, self.template_name, {'form': form})


class FileListView(LoginRequiredMixin, DataMixin, ListView):
    model = File
    template_name = 'base/file_list.html'
    success_url = reverse_lazy('file')
    login_url = reverse_lazy('login')
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(**kwargs)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        user = self.request.user.id
        file_list = File.objects.filter(author=user)
        return file_list


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'base/feedback.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(**kwargs)
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        email = form.cleaned_data['email']
        content = form.cleaned_data['content']
        try:
            send_mail(subject, content,
                      EMAIL_HOST_USER, [email])
        except BadHeaderError:
            return HttpResponse('Ошибка в теме письма.')


class LoginUser(DataMixin, LoginView):
    form_class = LoginForm
    template_name = 'base/login.html'
    success_url = reverse_lazy('user-page')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(**kwargs)
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegistrationForm
    model = Profile
    template_name = 'register/registration.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(**kwargs)
        return dict(list(context.items()) + list(c_def.items()))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Подтверждение регистрации. AvdBASE'
            message = render_to_string('register/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            messages.add_message(self.request, messages.INFO, 'Откройте сообщение на почте')
            messages.success(request, 'Пожалуйста перейдите по этой ссылке для подтверждения регистрации.')

            return redirect('login')

        return render(request, self.template_name, {'form': form})


class PasswordView(DataMixin, PasswordResetView):
    template_name = 'register/password_reset.html'
    email_template_name = 'base/password_reset_email.html'
    subject_template_name = 'base/password_reset_confirm.html'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('user-page')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(**kwargs)
        return dict(list(context.items()) + list(c_def.items()))


class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Profile.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, 'Вы подтвердили свой аккаунт. Спасибо')
            return redirect('user_page')
        else:
            messages.warning(request, 'Ошибка. Такой пользователь уже существует')
            return redirect('home')


def logout_user(request):
    logout(request)
    return redirect('home')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
