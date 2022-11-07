from django.conf.urls import url
from django.urls import path, include
from schema_graph.views import Schema
from django.contrib.auth import views as auth_views

from formation_metier.views import IndexView, HomeView, NewFormationFormView, DetailFormation, DetailSession, \
    UpdateFormationView, UpdateSessionView, NewSessionFormView, delete_session, delete_formation, PersonAutoComplete, \
    delete_registration, DetailSessionView

app_name = 'formation_metier'
urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('home/', HomeView.as_view(), name='home'),
    path('new_formation/', NewFormationFormView.as_view(), name='new_formation'),
    path('formation/<int:formation_id>/', DetailFormation.as_view(), name='detail_formation'),
    path('formation/new_session/<int:formation_id>', NewSessionFormView.as_view(), name='new_session'),
    path('formation/update/<int:formation_id>/', UpdateFormationView.as_view(), name='update_formation'),
    path('formation/session/update/<int:session_id>/', UpdateSessionView.as_view(), name='update_session'),
    path('formation/session/<int:session_id>/', DetailSessionView.as_view(), name='detail_session'),
    path('formation/session/delete/<int:session_id>/', delete_session, name='delete_session'),
    path('formation/session/register/delete/<int:register_id>', delete_registration, name='delete_registration'),
    path('formation/delete/<int:formation_id>/', delete_formation, name='delete_formation'),
    path('autocompletePerson/', PersonAutoComplete.as_view(), name='widget_participant'),

    # auth
    path('accounts/login/', auth_views.LoginView.as_view()),
    # graph_models
    path("schema/", Schema.as_view(), name='schemaModels'),
    # debug Toolbar
    path('__debug__/', include('debug_toolbar.urls')),
]
