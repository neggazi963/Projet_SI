from django.shortcuts import get_object_or_404, redirect, render

from app1.forms import EvaluationForm
from app1.models import Evaluation



#Gerer les evaluations 
def gestion_evaluations(request):

    evaluations = Evaluation.objects.select_related('employe').all()  # Chargement des évaluations avec les employés

    if 'search' in request.GET:
        search_query = request.GET['search']
        evaluations = evaluations.filter(employe__nom__icontains=search_query)

    context = {
        'evaluations': evaluations,
    }
    return render(request, 'evaluation_templates/gestion_evaluations.html', context)

from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import permission_required

# Gerer l'ajout d'une évaluation
def ajouter_evaluation(request):


    if request.method == 'POST':
        form = EvaluationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_evaluations')  # Redirige vers la gestion des évaluations
    else:
        form = EvaluationForm()
    return render(request, 'evaluation_templates/ajouter_evaluation.html', {'form': form})

#Gerer la modification d'une évaluation
def modifier_evaluation(request, pk):


    evaluation = get_object_or_404(Evaluation, pk=pk)
    if request.method == 'POST':
        form = EvaluationForm(request.POST, instance=evaluation)
        if form.is_valid():
            form.save()
            return redirect('gestion_evaluations')
    else:
        form = EvaluationForm(instance=evaluation)
    return render(request, 'evaluation_templates/modifier_evaluation.html', {'form': form})

# Gerer la suppression d'une évaluation
def supprimer_evaluation(request, pk):


    evaluation = get_object_or_404(Evaluation, pk=pk)
    if request.method == 'POST':
        evaluation.delete()
        return redirect('gestion_evaluations')
    return render(request, 'evaluation_templates/supprimer_evaluation.html', {'evaluation': evaluation})

# Gerer la consultation d'une évaluation
def consulter_evaluation(request, pk):

    evaluation = get_object_or_404(Evaluation, pk=pk)
    return render(request, 'evaluation_templates/consulter_evaluation.html', {'evaluation': evaluation})