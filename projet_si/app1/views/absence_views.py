from django.shortcuts import get_object_or_404, redirect, render
from app1.forms import AbsenceForm
from app1.models import Absence, Conge, Employe


def gestion_absence(request):
    employes = Employe.objects.all()
    absences = Absence.objects.select_related('employe').all()

    if 'search' in request.GET:
        search_query = request.GET['search']
        absences = absences.filter(employe__nom__icontains=search_query)

    context = {
        'employes': employes,
        'absences': absences,
    }
    return render(request, 'absence_templates/gestion_absence.html', context)


def ajouter_absence(request):
    if request.method == 'POST':
        form = AbsenceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_absence')
    else:
        form = AbsenceForm()
    return render(request, 'absence_templates/ajouter_absence.html', {'form': form})

# Vue pour afficher les absences d'un employé
def afficher_absences(request):
    absences = Conge.objects.all()  # Récupère toutes les absences
    return render(request, 'absence_templates/afficher_absences.html', {'absences': absences})


def supprimer_absence(request, pk):
    absence = get_object_or_404(Absence, pk=pk)
    absence.delete()
    return redirect('gestion_absence')


def modifier_absence(request, pk):
    absence = get_object_or_404(Absence, pk=pk)
    if request.method == 'POST':
        form = AbsenceForm(request.POST, instance=absence)
        if form.is_valid():
            form.save()
            return redirect('gestion_absence')
    else:
        form = AbsenceForm(instance=absence)
    return render(request, 'absence_templates/modifier_absence.html', {'form': form})


def consulter_absences(request):
    query = request.GET.get('q', '')
    absences = Absence.objects.all()
    if query:
        absences = absences.filter(employe__nom__icontains=query)

    context = {
        'absences': absences,
        'query': query
    }
    return render(request, 'absence_templates/consulter_absences.html', context)