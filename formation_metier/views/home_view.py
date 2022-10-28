from django.views import generic


class HomeView(generic.TemplateView):
    template_name = 'formation_metier/home.html'
