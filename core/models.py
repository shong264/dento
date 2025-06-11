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
    
# نموذج موعد

class Appointment(models.Model):
    patient = models.ForeignKey(Patient , on_delete=models.CASCADE , verbose_name="المريض")
    date = models.DateField(verbose_name="تاريخ الموعد")
    time =models.TimeField(verbose_name="وقت الموعد")
    notes = models.CharField(blank=True ,null=True ,max_length=250 , verbose_name="ملاحظات")
    created_at =models.DateTimeField(auto_now_add=True ,verbose_name="تاريخ الانشاء")

    class Meta:
        verbose_name = "موعد"
        verbose_name_plural = "المواعيد"

        def __str__(self):
            return f"{self.date} - {self.time}"

    


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