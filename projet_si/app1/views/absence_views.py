from django.shortcuts import get_object_or_404, redirect, render
from app1.forms import AbsenceForm
from app1.models import Absence, Conge, Employe

# Gerer la liste des absences
def gestion_absence(request):
    employes = Employe.objects.all() #La liste de tous les absneces
    absences = Absence.objects.select_related('employe').all()

    if 'search' in request.GET:
        search_query = request.GET['search']
        absences = absences.filter(employe__nom__icontains=search_query)

    context = {
        'employes': employes,
        'absences': absences,
    }
    return render(request, 'absence_templates/gestion_absence.html', context)

# Gerer l'ajout d'une absence
def ajouter_absence(request):
    if request.method == 'POST':
        form = AbsenceForm(request.POST)
        if form.is_valid():
            form.save()  #Sauvegarder l'absence
            return redirect('gestion_absence')  #Rediriger vers la liste des absences
    else:
        form = AbsenceForm()
    return render(request, 'absence_templates/ajouter_absence.html', {'form': form})



#Gerer la suppression d'une absence
def supprimer_absence(request, pk):
    absence = get_object_or_404(Absence, pk=pk)
    absence.delete()  #supprimer l'absence
    return redirect('gestion_absence')  #Rediriger vers la liste des absences


#Gerer la modification d'une absence
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


#Gerer la consultation d'une absence
def consulter_absence(request, id):
    absence = get_object_or_404(Absence, pk=id)

    context = {
        'absence': absence,
    }
    return render(request, 'absence_templates/consulter_absence.html', context)

