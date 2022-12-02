from django.urls import path, include
from schema_graph.views import Schema
from django.contrib.auth import views as auth_views

from formation_metier.views import ListFormationView, HomeView, NewFormationFormView, DetailFormation, \
    DetailSeanceView, UpdateFormationView, UpdateSeanceView, NewSeanceFormView, DeleteSeance, \
    DeleteFormation, PersonAutoComplete, DeleteRegister, add_self_registration
from formation_metier.api import urls_api

app_name = 'formation_metier'
urlpatterns = [
    path('', HomeView.as_view(), name=HomeView.name),
    path('list_formation/', ListFormationView.as_view(), name=ListFormationView.name),
    # detail_view
    path('formation/<uuid:formation_id>/', DetailFormation.as_view(), name=DetailFormation.name),
    path('formation/seance/<uuid:seance_id>/', DetailSeanceView.as_view(), name=DetailSeanceView.name),
    # new_view
    path('new_formation/', NewFormationFormView.as_view(), name=NewFormationFormView.name),
    path('formation/new_seance/<uuid:formation_id>', NewSeanceFormView.as_view(), name=NewSeanceFormView.name),
    path('formation/seance/<uuid:seance_id>', add_self_registration, name='add_self_registration'),
    # update_view
    path('formation/update/<uuid:formation_id>/', UpdateFormationView.as_view(), name=UpdateFormationView.name),
    path('formation/seance/update/<uuid:seance_id>/', UpdateSeanceView.as_view(), name=UpdateSeanceView.name),
    # delete_view
    path('formation/delete/<uuid:formation_id>/', DeleteFormation.as_view(), name='delete_formation'),
    path('formation/seance/delete/<uuid:seance_id>/', DeleteSeance.as_view(), name='delete_seance'),
    path('formation/seance/register/delete/', DeleteRegister.as_view(), name='delete_registration'),
    # Autocomplete Widget
    path('autocompletePerson/', PersonAutoComplete.as_view(), name=PersonAutoComplete.name),
    # API
    path('', include(urls_api)),
    # auth
    path('accounts/login/', auth_views.LoginView.as_view()),
    # graph_models
    path("schema/", Schema.as_view(), name='schemaModels'),
]
