from django import forms
from .models import Patient , Appointment
from django.utils import timezone

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name' , 'phone' , 'address' , 'date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }

class AppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        patient_id = kwargs.pop('patient_id', None)
        super().__init__(*args, **kwargs)
        
        # تحسين عرض حقل المريض
        self.fields['patient'].widget.attrs.update({
            'class': 'form-select'
        })
        
        if patient_id:
            self.fields['patient'].queryset = Patient.objects.filter(id=patient_id)
            self.fields['patient'].initial = patient_id
            self.fields['patient'].widget.attrs['disabled'] = True
            self.fields['patient'].required = False

    class Meta:
        model = Appointment
        fields = ['patient' , 'date' , 'time' , 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'})
        }
