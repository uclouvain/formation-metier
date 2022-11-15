from django.urls import path
from formation_metier.api import views

urlpatterns = [
    path('person/', views.PersonList.as_view()),
    path('person/<int:pk>/', views.PersonDetail.as_view()),
]
