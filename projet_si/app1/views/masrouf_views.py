from django.shortcuts import get_object_or_404, redirect, render

from app1.forms import MasroufForm
from app1.models import Employe, Masrouf


def gestion_masrouf(request):
    employes = Employe.objects.all()
    masroufs = Masrouf.objects.select_related('employe').all()

    if 'search' in request.GET:
        search_query = request.GET['search']
        masroufs = masroufs.filter(employe__nom__icontains=search_query)

    context = {
        'employes': employes,
        'masroufs': masroufs,
    }
    return render(request, 'masrouf_templates/gestion_masrouf.html', context)


# Ajouter, modifier et supprimer des entités
def ajouter_masrouf(request):
    if request.method == 'POST':
        form = MasroufForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_masrouf')
    else:
        form = MasroufForm()
    return render(request, 'masrouf_templates/ajouter_masrouf.html', {'form': form})


def supprimer_masrouf(request, pk):
    masrouf = get_object_or_404(Masrouf, pk=pk)
    masrouf.delete()
    return redirect('gestion_masrouf')



def modifier_masrouf(request, pk):
    masrouf = get_object_or_404(Masrouf, pk=pk)
    if request.method == 'POST':
        form = MasroufForm(request.POST, instance=masrouf)
        if form.is_valid():
            form.save()
            return redirect('gestion_masrouf')
    else:
        form = MasroufForm(instance=masrouf)
    return render(request, 'masrouf_templates/modifier_masrouf.html', {'form': form})    


def consulter_masroufs(request):
    query = request.GET.get('q', '')
    masroufs = Masrouf.objects.all()
    if query:
        masroufs = masroufs.filter(employe__nom__icontains=query)

    context = {
        'masroufs': masroufs,
        'query': query
    }
    return render(request, 'masrouf_templates/consult_masroufs.html', context)