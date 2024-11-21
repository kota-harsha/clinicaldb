"""
URL configuration for clinicals project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from clinicalsApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),

    path('patient/', views.PatientListView.as_view(), name='patient'),
    path('create-patient/', views.PatientCreateView.as_view()),
    path('update-patient/<int:pk>', views.PatientUpdateView.as_view()),
    path('delete-patient/<int:pk>', views.PatientDeleteView.as_view()),

    path('doctor/', views.DoctorListView.as_view(), name='doctor'),
    path('create-doctor/', views.DoctorCreateView.as_view()),
    path('update-doctor/<int:pk>', views.DoctorUpdateView.as_view()),
    path('delete-doctor/<int:pk>', views.DoctorDeleteView.as_view()),

    path('addData/<int:pk>/', views.addData),
    path('analyze/<int:pk>', views.analyze, name = 'analyze'),
    path('update-clinical-data/<int:pk>/', views.ClinicalDataUpdateView.as_view(), name='update_clinical_data'),
    path('delete-clinical-data/<int:pk>/', views.ClinicalDataDeleteView.as_view(), name='delete_clinical_data'),

    path('visit/', views.VisitListView.as_view(), name='visit_list'),
    path('create-visit/', views.VisitCreateView.as_view()),
    path('update-visit/<int:pk>', views.VisitUpdateView.as_view()),
    path('delete-visit/<int:pk>', views.VisitDeleteView.as_view()),
]
