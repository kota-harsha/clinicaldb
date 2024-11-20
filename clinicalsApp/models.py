from django.db import models

# Create your models here.

class Patient(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    GENDER = [('Male', 'male'),('Female','female'),('Other','other')]
    gender = models.CharField(choices=GENDER, max_length=10)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    medical_history = models.CharField(max_length=100)

class Doctor(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    department = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    data_of_birth = models.DateField()
    email = models.EmailField()
    clinic_history = models.TextField(max_length=100)

class ClinicalData(models.Model):
    COMPONENT_NAME = [('hw','Height / Weight'), ('bp', 'Blood Pressure'), ('hr', 'Heart Rate')]
    componentName = models.CharField(choices=COMPONENT_NAME, max_length=20)
    componentValue = models.CharField(max_length=20)
    measuredDataTime = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
