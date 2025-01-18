from pyexpat.errors import messages

from django.shortcuts import get_object_or_404, redirect, render
from app1.models import Conge
from app1.forms import CongeForm

#Gerer l'ajout d'un conge
def ajouter_conge(request):
    """
    Permet d'ajouter un nouveau congé.
    Accessible uniquement aux utilisateurs connectés.
    """
    if request.method == 'POST':
        form = CongeForm(request.POST)
        if form.is_valid():
            conge = form.save(commit=False)
            
            if conge.date_debut > conge.date_fin:
                messages.error(request, "La date de début ne peut pas être après la date de fin.")
            else:
                conge.save()
                
                return redirect('recherche_conge')
    else:
        form = CongeForm()
    return render(request, 'conge_templates/ajouter_conge.html', {'form': form})

#Gerer la modification d'un conge
def modifie_conge(request, conge_id):
    conge = get_object_or_404(Conge, id=conge_id)

    if request.method == 'POST':
        form = CongeForm(request.POST, instance=conge)
        if form.is_valid():
            form.save()  # Enregistrer les modifications
            return redirect('recherche_conge')  # Rediriger vers la liste des congés
    else:
        form = CongeForm(instance=conge)

    context = {
        'form': form,
        'conge': conge,
    }
    return render(request, 'conge_templates/modifie_conge.html', context)


#Gerer la suppression d'un conge
def supprime_conge(request, conge_id):
    conge = get_object_or_404(Conge, id=conge_id)

    if request.method == 'POST':
        conge.delete()  # Supprimer le congé
        return redirect('recherche_conge')  # Rediriger vers la liste des congés

    context = {
        'conge': conge,
    }
    return render(request, 'conge_templates/supprime_conge.html', context)

    
def recherche_conge(request):
    query = request.GET.get('q', '')
    
    if query:
        conges = Conge.objects.filter(employe__nom__icontains=query)  # Filtrer par nom de l'employé
    else:
        conges = Conge.objects.all()  # Récupérer tous les congés

    context = {
        'conges': conges,
        'query': query,
    }
    return render(request, 'conge_templates/recherche_conge.html', context)

def details_conge(request,conge_id):
    """
    Affiche les détails d'un congé spécifique.
    """
    conge = get_object_or_404(Conge,id=conge_id)
    return render(request, 'conge_templates/details_conge.html', {'conge': conge})