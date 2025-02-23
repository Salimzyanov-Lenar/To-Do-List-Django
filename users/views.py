import logging
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileUpdateForm
from django.contrib.auth import get_user_model
from django.db import IntegrityError


User = get_user_model()

logger = logging.getLogger(__name__)


class UserProfileView(TemplateView):
    """ Профиль пользователя """
    template_name = 'users/user_profile.html'
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('profile_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.request.user.profile)
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        else:
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)


class UserLoginView(LoginView):
    """ Страница аутентификации """
    template_name = 'users/login.html'
    form_class = CustomAuthenticationForm

    def form_valid(self, form):
        messages.success(self.request, "Вы успешно вошли!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Неправильный email или пароль.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('tasks_list')


class UserRegisterView(CreateView):
    """ Страница регистрации """
    model = User
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("login_page")

    def form_valid(self, form):
        try:
            user = form.save()
            login(self.request, user)  # Автоматический вход после регистрации
            messages.success(self.request, "Аккаунт успешно создан!")
            return redirect(self.success_url)
        except IntegrityError:
            messages.error(self.request, "Имя пользователя уже занято. Пожалуйста, выберите другое.")
            return self.form_invalid(form)


    def form_invalid(self, form):
        messages.error(self.request, "Ошибка регистрации. Проверьте данные.")
        return super().form_invalid(form)


def logout_view(request):
    logout(request)  # Выход пользователя
    return redirect('login_page')  # Редирект на страницу входа
