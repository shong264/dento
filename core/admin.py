from django.contrib import admin
from .models import Patient , Appointment

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
