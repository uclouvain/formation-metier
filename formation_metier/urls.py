from django.urls import path, include
from schema_graph.views import Schema
from django.contrib.auth import views as auth_views

from formation_metier.views import IndexView, HomeView, NewFormationFormView, DetailFormation, DetailSession, \
    UpdateFormationView, UpdateSessionView, NewSessionFormView

app_name = 'formation_metier'
urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('home/', HomeView.as_view(), name='home'),
    path('new_formation/', NewFormationFormView.as_view(), name='new_formation'),
    path('formation/<int:formation_id>/', DetailFormation.as_view(), name='detail_formation'),
    path('formation/new_session/<int:formation_id>', NewSessionFormView.as_view(), name='new_session'),
    path('formation/update/<int:formation_id>/', UpdateFormationView.as_view(), name='update_formation'),
    path('formation/session/update/<int:session_id>/', UpdateSessionView.as_view(), name='update_formation'),
    path('formation/session/<int:session_id>/', DetailSession.as_view(), name='detail_session'),

    # auth
    path('accounts/login/', auth_views.LoginView.as_view()),
    # graph_models
    path("schema/", Schema.as_view(), name='schemaModels'),
    # debug Toolbar
    path('__debug__/', include('debug_toolbar.urls')),
]
