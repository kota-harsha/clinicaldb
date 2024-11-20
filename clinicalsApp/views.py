from django.shortcuts import render, redirect
from clinicalsApp.models import Patient, ClinicalData, Doctor
from clinicalsApp.forms import ClinicalDataForm
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.urls import reverse_lazy

# Create your views here.

class PatientListView(ListView):
    model=Patient

class PatientCreateView(CreateView):
    model= Patient
    success_url = reverse_lazy('patient')
    fields = '__all__'

class PatientUpdateView(UpdateView):
    model= Patient
    success_url = reverse_lazy('patient')
    fields= '__all__'

class PatientDeleteView(DeleteView):
    model= Patient
    success_url = reverse_lazy('patient')


class DoctorListView(ListView):
    model=Doctor

class DoctorCreateView(CreateView):
    model= Doctor
    success_url = reverse_lazy('doctor')
    fields = '__all__'

class DoctorUpdateView(UpdateView):
    model= Doctor
    success_url = reverse_lazy('doctor')
    fields= '__all__'

class DoctorDeleteView(DeleteView):
    model= Doctor
    success_url = reverse_lazy('doctor')



def index(request):
    return render(request, 'clinicalsApp/index.html')







# **kwargs gets the varibale value from the url that requests for this view
def addData(request, **kwargs):
    form = ClinicalDataForm()
    patient = Patient.objects.get(id=kwargs['pk'])
    if request.method=='POST':
        form = ClinicalDataForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
    return render(request, 'clinicalsApp/clinical_data_form.html', {'form':form, 'patient':patient})

def analyze(request, **kwargs):
    data = ClinicalData.objects.filter(patient_id=kwargs['pk'])
    responseData = []
    for entry in data:
        if entry.componentName=='hw':
            haw = entry.componentValue.split('/')
            if len(haw) > 1:
                heightinmeter=float(haw[0]) * 0.4536
                BMI = (float(haw[1])) / (heightinmeter * heightinmeter)
                bmiEntry = ClinicalData()
                bmiEntry.componentName = 'BMI'
                bmiEntry.componentValue = BMI
                responseData.append(bmiEntry)
        responseData.append(entry)
    return render(request, 'clinicalsApp/generate_report.html', {'data': responseData})