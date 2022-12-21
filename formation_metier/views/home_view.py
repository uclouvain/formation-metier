from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic


class HomeView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'formation_metier/home.html'
    name = 'home'
