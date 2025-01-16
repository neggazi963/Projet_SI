from django.shortcuts import get_object_or_404, redirect, render
from app1.forms import EmployeForm
from app1.models import Employe


def rechercher_employe(request):
    query = request.GET.get('q', '')
    if query:
        employees = Employe.objects.filter(nom__icontains=query)  # Filtrer par nom
    else:
        employees = Employe.objects.all()  # Récupérer tous les employés

    if request.method == 'POST':
        form = EmployeForm(request.POST)
        if form.is_valid():
            form.save()  # Enregistrer un nouvel employé
            return redirect('rechercher_employe')  # Rediriger vers la même page
    else:
        form = EmployeForm()

    context = {
        'employees': employees,
        'form': form,
        'query': query,
    }
    return render(request, 'employe_templates/rechercher_employe.html', context)


def insert_employe(request):
    if request.method == 'POST':
        form = EmployeForm(request.POST) 
        if form.is_valid():
            form.save()  # Enregistrer le nouvel employé
            return redirect('rechercher_employe')  # Rediriger vers la liste des employés
    else:
        form = EmployeForm()

    context = {
        'form': form,
    }
    return render(request, 'employe_templates/insert_employe.html', context)





def modifier_employe(request, employe_id):
    employe = get_object_or_404(Employe, id=employe_id)

    if request.method == 'POST':
        form = EmployeForm(request.POST, instance=employe)
        if form.is_valid():
            form.save()  # Enregistrer les modifications
            return redirect('rechercher_employe')  
    else:
        form = EmployeForm(instance=employe)

    context = {
        'form': form,
        'employe': employe,
    }
    return render(request, 'employe_templates/modifie_employe.html', context)



def supprimer_employe(request, employe_id):
    employe = get_object_or_404(Employe, id=employe_id)

    if request.method == 'POST':
        employe.delete()  
        return redirect('rechercher_employe')  # Rediriger vers la liste des employés

    context = {
        'employe': employe,
    }
    return render(request, 'employe_templates/supprime_employe.html', context)



def consult_employe(request, employe_id):
    employe = get_object_or_404(Employe, id=employe_id)  

    context = {
        'employe': employe,
    }
    return render(request, 'employe_templates/consult_employe.html', context)

def afficher_employes(request):
   employes = Employe.objects.all()
   return render(request, "employe_templates/list_employes.html", {"employes": employes})  # Remplacé 'Employes' par 'employes'