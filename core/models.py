from django.db import models

# Create your models here.


# نموذج مريض
class Patient(models.Model):
    name = models.CharField(max_length =250 , verbose_name="اسم المريض")
    phone = models.CharField(max_length=20 , verbose_name="رقم الهاتف")
    address = models.CharField(blank=True ,null=True ,max_length=250 , verbose_name="العنوان")
    date_of_birth = models.DateField(blank=True ,null=True , verbose_name="تاريخ الميلاد")
    created_at =models.DateTimeField(auto_now_add=True ,verbose_name="تاريخ الانشاء")

    class Meta:
        verbose_name = "مريض"
        verbose_name_plural = "المرضى"


    def __str__(self):
        return self.name
    

class Doctor(models.Model):
    name = models.CharField(max_length=250, verbose_name="اسم الطبيب")
    # Add any other fields that are relevant to the Doctor model

    class Meta:
        verbose_name = "طبيب"
        verbose_name_plural = "الأطباء"

    def __str__(self):
        return self.name
    
# نموذج موعد

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name="المريض")
    doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الطبيب")  # هذا السطر يجب أن يكون موجودًا
    date = models.DateField(verbose_name="تاريخ الموعد")
    time = models.TimeField(verbose_name="وقت الموعد")
    notes = models.CharField(blank=True, null=True, max_length=250, verbose_name="ملاحظات")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    class Meta:
        verbose_name = "موعد"
        verbose_name_plural = "المواعيد"

    def __str__(self):
        return f"{self.patient.name} - {self.date} - {self.time}"

        


    


# models.py (إضافة هذا النموذج)
class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name="المريض")
    visit_date = models.DateField(auto_now_add=True, verbose_name="تاريخ الزيارة")
    diagnosis = models.TextField(verbose_name="التشخيص")
    treatment = models.TextField(verbose_name="العلاج")
    prescription = models.TextField(blank=True, verbose_name="الوصفة الطبية")
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="التكلفة")

    class Meta:
        verbose_name = "ملف طبي"
        verbose_name_plural = "الملفات الطبية"

# أنواع العلاجات (إضافة ديناميكية)

class DentalRecord(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, verbose_name="الملف الطبي")
    problematic_teeth = models.CharField(max_length=250, verbose_name="الأسنان التي بها مشكلة")  # مثال: "11, 12, 21"
    notes = models.TextField(blank=True, null=True, verbose_name="ملاحظات")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")

    class Meta:
        verbose_name = "رسم الأسنان"
        verbose_name_plural = "رسومات الأسنان"

    def __str__(self):
        return f"{self.medical_record.patient.name} - {self.medical_record.visit_date}"
    
TOOTH_CHOICES = [(i, f'Tooth {i}') for i in range(11, 49) if not str(i)[1] in ['9', '0']]

class ToothRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    tooth_number = models.IntegerField(choices=TOOTH_CHOICES)
    condition = models.CharField(max_length=100)  # مثلاً: سليم، تسوس، مخلوع
    treatment_plan = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} - Tooth {self.tooth_number}"

