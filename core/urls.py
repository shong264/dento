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


    path('dashboard/medical-records/', views.medical_records_list, name='medical_records_list'),
    path('dashboard/add-medical-record/', views.add_medical_record, name='add_medical_record'),
    path('dashboard/medical-record/edit/<int:pk>/', views.edit_medical_record, name='edit_medical_record'),
    path('dashboard/medical-record/delete/<int:pk>/', views.delete_medical_record, name='delete_medical_record'),


    path('add-dental-record/', views.add_dental_record, name='add_dental_record'),
    
    path('exam/<int:patient_id>/', views.dental_exam_view, name='dental_exam'),
    path('add-or-update-tooth/<int:patient_id>/', views.add_or_update_tooth_record, name='add_or_update_tooth_record'),
    path('edit-tooth/<int:record_id>/', views.edit_tooth_record, name='edit_tooth_record'),
    path('delete-tooth/<int:record_id>/', views.delete_tooth_record, name='delete_tooth_record'),




  


    







 


]
