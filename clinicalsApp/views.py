from django.shortcuts import render, redirect, get_object_or_404
from clinicalsApp.models import Patient, ClinicalData, Doctor, Visit
from clinicalsApp.forms import ClinicalDataForm, VisitForm
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.db import connection
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from django.http import JsonResponse

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
    success_url = reverse_lazy('analyze')  

    def get_success_url(self):
        return reverse_lazy('analyze', kwargs={'pk': self.object.patient.id})
    
class ClinicalDataUpdateView(UpdateView):
    model = ClinicalData
    fields = '__all__'
    template_name = 'clinicalsApp/clinical_data_form.html'
    success_url = reverse_lazy('analyze')

    def get_success_url(self):
        return reverse_lazy('analyze', kwargs={'pk': self.object.patient.id})

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

class VisitListView(ListView):
    model = Visit
    template_name = 'clinicalsApp/visit_list.html'

    def get_queryset(self):
        return Visit.objects.select_related('doctor', 'patient')

class VisitCreateView(CreateView):
    model = Visit
    form_class = VisitForm
    success_url = reverse_lazy('visit_list')

class VisitUpdateView(UpdateView):
    model = Visit
    form_class = VisitForm
    success_url = reverse_lazy('visit_list')

class VisitDeleteView(DeleteView):
    model = Visit
    success_url = reverse_lazy('visit_list')

def execute_raw_sql(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params or [])
        if query.strip().lower().startswith('select'):
            return dictfetchall(cursor)
    return None

def dictfetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]



@csrf_exempt
def vulnerable_select(request):
    if request.method == 'POST':
        name = request.POST.get('firstName', '')
        with connection.cursor() as cursor:
            # Vulnerable query - for demonstration only
            query = f"SELECT id, firstName, lastName, age, address FROM clinicalsapp_patient WHERE firstName = '{name}'"
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            patients = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return JsonResponse({'patients': patients})
    return render(request, 'clinicalsApp/vulnerable_select.html')

@csrf_exempt
def vulnerable_update(request):
    if request.method == 'POST':
        patient_id = request.POST.get('id', '')
        new_address = request.POST.get('address', '')
        with connection.cursor() as cursor:
            # Vulnerable query - for demonstration only
            query = f"UPDATE clinicalsapp_patient SET address = '{new_address}' WHERE id = {patient_id}"
            cursor.execute(query)
        return JsonResponse({'status': 'updated'})
    return render(request, 'clinicalsApp/vulnerable_update.html')

def secure_select(request):
    if request.method == 'POST':
        name = request.POST.get('firstName', '')
        with connection.cursor() as cursor:
            # Secure query using prepared statement
            query = "SELECT id, firstName, lastName, age, address FROM clinicalsapp_patient WHERE firstName = %s"
            cursor.execute(query, [name])
            columns = [col[0] for col in cursor.description]
            patients = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return JsonResponse({'patients': patients})
    return render(request, 'clinicalsApp/secure_select.html')
