from django.shortcuts import render, redirect
from clinicalsApp.models import Patient, ClinicalData, Doctor
from clinicalsApp.forms import ClinicalDataForm
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

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

class ClinicalDataDeleteView(DeleteView):
    model = ClinicalData
    # template_name = 'clinicalsApp/delete_clinical_data.html'
    success_url = reverse_lazy('analyze')  

    def get_success_url(self):
        # Redirect back to the analyze page for the specific patient
        return reverse_lazy('analyze', kwargs={'pk': self.object.patient.id})
    
class ClinicalDataUpdateView(UpdateView):
    model = ClinicalData
    fields = '__all__'
    template_name = 'clinicalsApp/clinical_data_form.html'
    success_url = reverse_lazy('analyze')  # Adjust to redirect to the analyze page

    def get_success_url(self):
        # Redirect back to the analyze page for the specific patient
        return reverse_lazy('analyze', kwargs={'pk': self.object.patient.id})

# **kwargs gets the varibale value from the url that requests for this view
def addData(request, **kwargs):
    form = ClinicalDataForm()
    patient = Patient.objects.get(id=kwargs['pk'])
    if request.method=='POST':
        form = ClinicalDataForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
    return render(request, 'clinicalsApp/clinicaldata_form.html', {'form':form, 'patient':patient})

def analyze(request, **kwargs):
    data = ClinicalData.objects.filter(patient_id=kwargs['pk'])
    responseData = []
    for entry in data:
        responseData.append(entry)
    return render(request, 'clinicalsApp/generate_report.html', {'data': responseData})