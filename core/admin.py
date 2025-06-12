from django.contrib import admin
from .models import Patient , Appointment , MedicalRecord ,Doctor , DentalRecord


# Register your models here.

class PatientAdmin(admin.ModelAdmin):
    list_display = ('name' , 'phone' , 'address' , 'date_of_birth')
    list_filter = ('name' ,  'date_of_birth')
    search_fields = ('name' , 'phone')
    
admin.site.register(Patient)


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient' , 'date' , 'time' , 'notes')
    list_filter = ('date' )
admin.site.register(Appointment)

class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient' , 'visit_date' , 'diagnosis' , 'treatment' , 'prescription' , 'cost')
    list_filter = ('patient' , 'visit_date')
    admin.site.register(MedicalRecord)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name',)


class DentalRecordAdmin(admin.ModelAdmin):
    list_display = ('medical_record', 'problematic_teeth', 'notes')
    list_filter = ('medical_record',)
    admin.site.register(DentalRecord)







