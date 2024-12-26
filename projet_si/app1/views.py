from django.shortcuts import get_object_or_404, redirect, render

from .forms import CongeForm
from .models import Employe,Conge
def afficher_employes(request):
   employes = Employe.objects.all()
   return render(request,"list_employes.html",{"Employes":employes})




def liste_conges(request):
    conges = Conge.objects.all()
    return render(request, 'conges/liste_conges.html', {'conges': conges})

def ajouter_conge(request):
    if request.method == 'POST':
        form = CongeForm(request.POST)
        if form.is_valid():
            conge = form.save(commit=False)
            conge.save()
            return redirect('liste_conges')
    else:
        form = CongeForm()
    return render(request, 'conges/ajouter_conge.html', {'form': form})

def details_conge(request, conge_id):
    conge = get_object_or_404(Conge, id=conge_id)
    return render(request, 'conges/details_conge.html', {'conge': conge})
