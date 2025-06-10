from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Patient , Appointment
from .forms import PatientForm , AppointmentForm
from datetime import date
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.db.models import Count

# Create your views here.

# نموذج المرضى
from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Patient, Appointment
from django.db import models

@login_required(login_url='login')
def dashboard(request):
    today = date.today()
    patients_count = Patient.objects.count()
    appointments_today = Appointment.objects.filter(date=today)
    upcoming_appointments = Appointment.objects.filter(date__gt=today).order_by('date', 'time')[:5]
    most_visited_patient = (
        Patient.objects.annotate(count=models.Count('appointment'))
        .order_by('-count')
        .first()
    )

    return render(request, 'core/dashboard.html', {
        'patients_count': patients_count,
        'appointments_today': appointments_today,
        'upcoming_appointments': upcoming_appointments,
        'most_visited_patient': most_visited_patient,
    })
@login_required(login_url='login')
def patient_list(request):
    # جلب جميع المرضى من قاعدة البيانات
    patients = Patient.objects.all()
    
    # تحضير البيانات للتمرير إلى القالب
    context = {
        'patients': patients
    }
    
    # عرض صفحة قائمة المرضى وتمرير البيانات
    return render(request, 'core/patient_list.html', context)

@login_required(login_url='login')
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ تم حفظ المريض بنجاح!')
            return redirect('dashboard')
    else:
        form = PatientForm()
    return render(request, 'core/add_patient.html', {'form': form})

@login_required(login_url='login')
def edit_patient(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ تم تعديل المريض بنجاح!')
            return redirect('dashboard')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'core/edit_patient.html', {'form': form})

@login_required(login_url='login')
def delete_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        messages.success(request, "🗑️ تم حذف المريض.")
        return redirect('patient_list')
    return render(request, 'core/delete_patient_confirm.html', {'patient': patient})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, '✅ تم تسجيل الدخول بنجاح!')
            return redirect('dashboard')
        else:
            messages.error(request, '❌ اسم المستخدم أو كلمة المرور غير صحيحة.')
    
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "👋 تم تسجيل الخروج بنجاح.")
    return redirect('login')








# نموذج موعد
@login_required(login_url='login')
def appointment_list(request):
    appointments = Appointment.objects.all()
    # تحضير البيانات للتمرير إلى القالب
    context = {
        'appointments': appointments
    }
    
    # عرض صفحة قائمة المرضى وتمرير البيانات
    return render(request, 'core/appointment_list.html', context)

@login_required(login_url='login')
def add_appointment(request, patient_id=None):
    patient = None
    if patient_id:
        patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, patient_id=patient_id)
        if form.is_valid():
            appointment = form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm(patient_id=patient_id)

    context = {
        'form': form,
        'patient': patient,
    }
    return render(request, 'core/add_appointment.html', context)

@login_required(login_url='login')
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ تم تعديل الموعد بنجاح!')
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'core/edit_appointment.html', {'form': form, 'appointment': appointment})


@login_required(login_url='login')
def delete_appointment(request, pk):    
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':    
        appointment.delete()
        messages.success(request, "🗑️ تم حذف الموعد.")
        return redirect('appointment_list')
    return render(request, 'core/delete_appointment_confirm.html', {'appointment': appointment})






@login_required(login_url='login')
def reports(request):
    today = date.today()

    # عدد المواعيد لكل مريض
    patient_appointments = Patient.objects.annotate(appointment_count=Count('appointment')).order_by('-appointment_count')

    # المواعيد المنتهية والقادمة
    past_appointments = Appointment.objects.filter(date__lt=today).count()
    upcoming_appointments = Appointment.objects.filter(date__gte=today).count()

    # أسماء المرضى وعدد زياراتهم للرسم البياني
    labels = [p.name for p in patient_appointments[:5]]
    data = [p.appointment_count for p in patient_appointments[:5]]

    context = {
        'labels': labels,
        'data': data,
        'past_appointments': past_appointments,
        'upcoming_appointments': upcoming_appointments,
    }
    return render(request, 'core/reports.html', context)
