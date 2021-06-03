from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login

from .models import CreationForm


class SignUp(CreateView):

    form_class = CreationForm
    success_url = reverse_lazy("index")
    template_name = "signup.html"

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid
