from django.urls import path
from formation_metier.api import views

urlpatterns = [
    path('employeucl/', views.EmployeUCLList.as_view()),
    path('employeucl/<int:pk>/', views.EmployeUCLDetail.as_view()),
]
