from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import JsonResponse
from .models import Patient, Appointment, MedicalRecord, ToothRecord ,  DentalRecord
from .forms import PatientForm, AppointmentForm, MedicalRecordForm, DentalRecordForm, ToothRecordForm

# ----------------------------
# 👤 تسجيل الدخول والخروج
# ----------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
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

# ----------------------------
# 🏠 لوحة التحكم
# ----------------------------
@login_required(login_url='login')
def dashboard(request):
    today = date.today()
    patients_count = Patient.objects.count()
    appointments_today = Appointment.objects.filter(date=today)
    upcoming_appointments = Appointment.objects.filter(date__gt=today).order_by('date', 'time')[:5]
    most_visited_patient = (
        Patient.objects.annotate(count=Count('appointment'))
        .order_by('-count')
        .first()
    )
    return render(request, 'core/dashboard.html', {
        'patients_count': patients_count,
        'appointments_today': appointments_today,
        'upcoming_appointments': upcoming_appointments,
        'most_visited_patient': most_visited_patient,
    })

# ----------------------------
# 👨‍⚕️ المرضى
# ----------------------------
@login_required(login_url='login')
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'core/patient_list.html', {'patients': patients})

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
    patient = get_object_or_404(Patient, id=patient_id)
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

# ----------------------------
# 📅 المواعيد
# ----------------------------
@login_required(login_url='login')
def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'core/appointment_list.html', {'appointments': appointments})

@login_required(login_url='login')
def add_appointment(request, patient_id=None):
    patient = get_object_or_404(Patient, id=patient_id) if patient_id else None
    if request.method == 'POST':
        form = AppointmentForm(request.POST, patient_id=patient_id)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm(patient_id=patient_id)
    return render(request, 'core/add_appointment.html', {'form': form, 'patient': patient})

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

# ----------------------------
# 📝 السجلات الطبية
# ----------------------------
@login_required(login_url='login')
def medical_records_list(request):
    query = request.GET.get('q')
    records = MedicalRecord.objects.select_related('patient')
    if query:
        records = records.filter(Q(patient__name__icontains=query))
    records = records.order_by('-visit_date')
    return render(request, 'core/medical_records_list.html', {'records': records, 'query': query})

@login_required(login_url='login')
def add_medical_record(request):
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medical_records_list')
    else:
        form = MedicalRecordForm()
    return render(request, 'core/add_medical_record.html', {'form': form})

@login_required(login_url='login')
def edit_medical_record(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk)
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('medical_records_list')
    else:
        form = MedicalRecordForm(instance=record)
    return render(request, 'core/edit_medical_record.html', {'form': form})

@login_required(login_url='login')
def delete_medical_record(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk)
    record.delete()
    return redirect('medical_records_list')

# ----------------------------
# 🦷 فحص الأسنان
# ----------------------------
@login_required(login_url='login')
def dental_exam_view(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    upper_teeth = list(range(18, 10, -1)) + list(range(21, 29))
    lower_teeth = list(range(48, 40, -1)) + list(range(31, 39))
    return render(request, 'core/dental_exam.html', {
        'patient': patient,
        'upper_teeth': upper_teeth,
        'lower_teeth': lower_teeth,
    })

@login_required(login_url='login')
def add_tooth_record(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = ToothRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.patient = patient
            record.save()
            return redirect('dental_exam', patient_id=patient.id)
    else:
        form = ToothRecordForm(initial={'tooth_number': request.GET.get('tooth_number')})
    return render(request, 'core/add_tooth_record.html', {'form': form, 'patient': patient})

@login_required(login_url='login')
def add_dental_record(request):
    if request.method == 'POST':
        form = DentalRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = DentalRecordForm()
    return render(request, 'core/dental_record_form.html', {'form': form})

# ----------------------------
# 📊 التقارير
# ----------------------------
@login_required(login_url='login')
def reports(request):
    today = date.today()
    patient_appointments = Patient.objects.annotate(appointment_count=Count('appointment')).order_by('-appointment_count')
    past_appointments = Appointment.objects.filter(date__lt=today).count()
    upcoming_appointments = Appointment.objects.filter(date__gte=today).count()

    labels = [p.name for p in patient_appointments[:5]]
    data = [p.appointment_count for p in patient_appointments[:5]]

    return render(request, 'core/reports.html', {
        'labels': labels,
        'data': data,
        'past_appointments': past_appointments,
        'upcoming_appointments': upcoming_appointments,
    })


TOOTH_NUMBERS = [i for i in range(11, 49) if not str(i)[1] in ['9', '0']]

@login_required(login_url='login')
def dental_exam_view(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    upper_teeth = [i for i in TOOTH_NUMBERS if i < 30]
    lower_teeth = [i for i in TOOTH_NUMBERS if i >= 30]
    tooth_records_qs = ToothRecord.objects.filter(patient=patient)
    tooth_records = {record.tooth_number: record for record in tooth_records_qs}

    return render(request, 'core/dental_exam.html', {
        'patient': patient,
        'upper_teeth': upper_teeth,
        'lower_teeth': lower_teeth,
        'tooth_records': tooth_records
    })



@login_required(login_url='login')
def add_or_update_tooth_record(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    tooth_number = request.POST.get("tooth_number")
    condition = request.POST.get("condition", "سليم")
    treatment_plan = request.POST.get("treatment_plan", "")
    notes = request.POST.get("notes", "")

    record, created = ToothRecord.objects.update_or_create(
        patient=patient,
        tooth_number=tooth_number,
        defaults={
            'condition': condition,
            'treatment_plan': treatment_plan,
            'notes': notes
        }
    )
    return redirect('dental_exam', patient_id=patient.id)


@login_required(login_url='login')
def edit_tooth_record(request, record_id):
    record = get_object_or_404(ToothRecord, id=record_id)
    if request.method == 'POST':
        record.condition = request.POST.get('condition')
        record.treatment_plan = request.POST.get('treatment_plan')
        record.notes = request.POST.get('notes')
        record.save()
        return redirect('dental_exam', patient_id=record.patient.id)

    return render(request, 'core/edit_tooth_record.html', {'record': record})


@login_required(login_url='login')
def delete_tooth_record(request, record_id):
    record = get_object_or_404(ToothRecord, id=record_id)
    patient_id = record.patient.id
    record.delete()
    return redirect('dental_exam', patient_id=patient_id)
