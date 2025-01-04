from django.shortcuts import get_object_or_404, redirect, render

from app1.forms import EvaluationForm
from app1.models import Evaluation


def gestion_evaluations(request):
    evaluations = Evaluation.objects.select_related('employe').all()  # Chargement des évaluations avec les employés

    if 'search' in request.GET:
        search_query = request.GET['search']
        evaluations = evaluations.filter(employe__nom__icontains=search_query)

    context = {
        'evaluations': evaluations,
    }
    return render(request, 'evaluation_templates/gestion_evaluations.html', context)

# Vue pour ajouter une évaluation
def ajouter_evaluation(request):
    if request.method == 'POST':
        form = EvaluationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_evaluations')  # Redirige vers la gestion des évaluations
    else:
        form = EvaluationForm()
    return render(request, 'evaluation_templates/ajouter_evaluation.html', {'form': form})

# Vue pour modifier une évaluation
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

# Vue pour supprimer une évaluation
def supprimer_evaluation(request, pk):
    evaluation = get_object_or_404(Evaluation, pk=pk)
    if request.method == 'POST':
        evaluation.delete()
        return redirect('gestion_evaluations')
    return render(request, 'evaluation_templates/supprimer_evaluation.html', {'evaluation': evaluation})

# Vue pour consulter une évaluation
def consulter_evaluation(request, pk):
    evaluation = get_object_or_404(Evaluation, pk=pk)
    return render(request, 'evaluation_templates/consulter_evaluation.html', {'evaluation': evaluation})