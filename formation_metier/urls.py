from django.conf.urls import url
from django.urls import path, include
from schema_graph.views import Schema
from django.contrib.auth import views as auth_views

from formation_metier.views import ListFormationView, HomeView, NewFormationFormView, DetailFormation, \
    DetailSessionView, UpdateFormationView, UpdateSessionView, NewSessionFormView, delete_session, delete_formation, \
    PersonAutoComplete, delete_registration
from formation_metier.api import urls_api

app_name = 'formation_metier'
urlpatterns = [
    path('', HomeView.as_view(), name=HomeView.name),
    path('list_formation/', ListFormationView.as_view(), name=ListFormationView.name),
    # detail_view
    path('formation/<int:formation_id>/', DetailFormation.as_view(), name=DetailFormation.name),
    path('formation/session/<int:session_id>/', DetailSessionView.as_view(), name=DetailSessionView.name),
    # new_view
    path('new_formation/', NewFormationFormView.as_view(), name=NewFormationFormView.name),
    path('formation/new_session/<int:formation_id>', NewSessionFormView.as_view(), name=NewSessionFormView.name),
    # update_view
    path('formation/update/<int:formation_id>/', UpdateFormationView.as_view(), name=UpdateFormationView.name),
    path('formation/session/update/<int:session_id>/', UpdateSessionView.as_view(), name=UpdateSessionView.name),
    # delete_view
    path('formation/delete/<int:formation_id>/', delete_formation, name='delete_formation'),
    path('formation/session/delete/<int:session_id>/', delete_session, name='delete_session'),
    path('formation/session/register/delete/<int:register_id>', delete_registration, name='delete_registration'),
    # Autocomplete Widget
    path('autocompletePerson/', PersonAutoComplete.as_view(), name=PersonAutoComplete.name),
    # API
    path('', include(urls_api)),
    # auth
    path('accounts/login/', auth_views.LoginView.as_view()),
    # graph_models
    path("schema/", Schema.as_view(), name='schemaModels'),
    # debug Toolbar
    path('__debug__/', include('debug_toolbar.urls')),
]
