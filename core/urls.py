from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('patient_list/', views.patient_list, name='patient_list'),
    path('patient_list/add-patient/', views.add_patient, name='add_patient'),
    path('edit_patient/edit/<int:patient_id>/', views.edit_patient, name='edit_patient'),
    path('delete_patient/delete/<int:pk>/', views.delete_patient, name='delete_patient'),

    path('appointment_list/', views.appointment_list, name='appointment_list'),
    path('appointment_list/add-appointment/', views.add_appointment, name='add_appointment'),
    path('edit_appointment/edit/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'),
    path('delete_appointment/delete/<int:pk>/', views.delete_appointment, name='delete_appointment'),


]
