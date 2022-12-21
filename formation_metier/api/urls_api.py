from django.urls import path
from formation_metier.api import views

urlpatterns = [
    path('employes_ucl/', views.EmployeUCLList.as_view()),
    path('employe_ucl/<uuid:pk>/', views.EmployeUCLDetail.as_view()),
]
