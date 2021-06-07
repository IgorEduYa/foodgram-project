from django.views.generic import CreateView
from django.contrib.auth.views import PasswordChangeView

from django.urls import reverse_lazy

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = "signup.html"


class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('index')
