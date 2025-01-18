from django.shortcuts import get_object_or_404, redirect, render
from app1.forms import ContratForm
from app1.models import Contrat

# Gérer l'ajout d'un nouveau contrat
def ajouter_contrat(request):
    if request.method == 'POST':
        form = ContratForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recherche_contrats')  # Rediriger vers la liste des congés
    else:
        form = ContratForm()
    return render(request, 'contrat_templates/ajouter_contrat.html', {'form': form})


def details_contrat(request, contrat_id):
    contrat = get_object_or_404(Contrat, id=contrat_id)
    return render(request, 'contrat_templates/details_contrat.html', {'contrat': contrat})


# Gérer la modification d'un contrat
def modifier_contrat(request, contrat_id):
    contrat = get_object_or_404(Contrat, id=contrat_id)
    if request.method == 'POST':
        form = ContratForm(request.POST, instance=contrat)
        if form.is_valid():
            form.save()
            return redirect('recherche_contrats')  # Rediriger vers la liste des congés
    else:
        form = ContratForm(instance=contrat)
    return render(request, 'contrat_templates/modifier_contrat.html', {'form': form})



  
# Gérer la suppression d'un contrat
def supprimer_contrat(request, contrat_id):
    contrat = get_object_or_404(Contrat, id=contrat_id)
    if request.method == 'POST':
        contrat.delete()  # Supprimer le congé
        return redirect('recherche_contrats')  # Rediriger vers la liste des congés
    context = {
        'contrat': contrat,
    }
    return render(request, 'contrat_templates/supprimer_contrat.html', context)

# Gérer la recherche d'un contrat
def recherche_contrats(request):
    
    query = request.GET.get('q', '')
    
   
    if query:
        contrats = Contrat.objects.filter(employe__nom__icontains=query)  # Filtrer par nom de l'employé
    else:
        contrats = Contrat.objects.all()  # Récupérer tous les contrats

    # Gérer l'ajout d'un nouveau contrat
    if request.method == 'POST':
        form = ContratForm(request.POST)
        if form.is_valid():
            form.save()  # Enregistrer le nouveau contrat
            return redirect('recherche_contrat')  # Rediriger vers la même page
    else:
        form = ContratForm()

    context = {
        'contrats': contrats,
        'form': form,
        'query': query,
    }
    return render(request, 'contrat_templates/recherche_contrats.html', context)