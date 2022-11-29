from django.urls import path
from formation_metier.api import views

urlpatterns = [
    path('employe_ucl/', views.EmployeUCLList.as_view()),
    path('employe_ucl/<int:pk>/', views.EmployeUCLDetail.as_view()),
]
