from django.shortcuts import render, redirect
from typing import Any, Dict
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import (
    render
)
from django.contrib.auth import (
    authenticate as dj_authenticate,
    login as dj_login,
    logout as dj_logout,
)
from django.views.generic import FormView

from auths.models import CustomUser, UserHobbies
from auths.forms import RegisterForm, LoginForm
from shop.models import Basket
# Create your views here.


class RegisterView(FormView):
    template_name = 'registration/sign_up.html'
    form_class = RegisterForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        hobbi = form.cleaned_data.get('hobbi').split(',')
        user = CustomUser.objects.create_user(email, password)
        for hob in hobbi:
            UserHobbies.objects.create(user=user, hobbies=hob)
        dj_login(self.request, user)
        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'registration/login.html'
    form_class = LoginForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = dj_authenticate(email=email, password=password)
        if user:
            dj_login(self.request, user)
        return super().form_valid(form)


class LogoutView(View):
    template_name = 'registration/login.html'

    def get(self,  request, *args: Any, **kwargs: Any):
        dj_logout(request)
        return redirect('/login')


def home(request):
    return render(request, "core/home.html")
