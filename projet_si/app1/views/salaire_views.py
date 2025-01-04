from django.shortcuts import get_object_or_404, redirect, render
from app1.forms import SalaireForm
from app1.models import Absence, Employe, Masrouf, Prime, Salaire


def calculer_salaire(employe):
    salaire_base = 30000
    total_primes = Prime.objects.filter(employe=employe).aggregate(Sum('montant'))['montant__sum'] or 0
    total_absences = Absence.objects.filter(employe=employe).aggregate(Sum('impact_salaire'))['impact_salaire__sum'] or 0
    total_masrouf = Masrouf.objects.filter(employe=employe).aggregate(Sum('montant'))['montant__sum'] or 0
    return salaire_base + total_primes - total_absences - total_masrouf


def gestion_salaire(request):
    employes = Employe.objects.all()
    salaires = Salaire.objects.select_related('employe').all()

    if 'search' in request.GET:
        search_query = request.GET['search']
        salaires = salaires.filter(employe__nom__icontains=search_query)

    context = {
        'employes': employes,
        'salaires': salaires,
    }
    return render(request, 'salaire_templates/gestion_salaire.html', context)


def ajouter_salaire(request):
    if request.method == "POST":
        form = SalaireForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_salaire')
    else:
        form = SalaireForm()
    return render(request, 'salaire_templates/ajouter_salaire.html', {'form': form})





def modifier_salaire(request, salaire_id):
    salaire = get_object_or_404(Salaire, id=salaire_id)
    if request.method == "POST":
        form = SalaireForm(request.POST, instance=salaire)
        if form.is_valid():
            form.save()
            return redirect('gestion_salaire')
    else:
        form = SalaireForm(instance=salaire)
    return render(request, 'salaire_templates/modifier_salaire.html', {'form': form})





def supprimer_salaire(request, salaire_id):
    salaire = get_object_or_404(Salaire, id=salaire_id)
    if request.method == "POST":
        salaire.delete()
        return redirect('gestion_salaire')
    return render(request, 'salaire_templates/supprimer_salaire.html', {'salaire': salaire})


from django.db.models import Sum

def consulter_salaire(request, employe_id):
    employe = get_object_or_404(Employe, id=employe_id)

    # Récupérer les objets Salaire associés
    salaires = employe.salaire_set.all()

    # Calculer le total des primes
    total_primes = employe.prime_set.aggregate(total=Sum('montant'))['total'] or 0

    # Calculer l'impact total des absences
    total_absences = employe.absence_set.aggregate(total=Sum('impact_salaire'))['total'] or 0

    # Calculer le total des masroufs
    total_masrouf = employe.masrouf_set.aggregate(total=Sum('montant'))['total'] or 0

    context = {
        'employe': employe,
        'salaires': salaires,
        'total_primes': total_primes,
        'total_absences': total_absences,
        'total_masrouf': total_masrouf,
        'salaire_base': 30000,  # Salaire de base (exemple)
    }
    return render(request, 'salaire_templates/consulter_salaire.html', context)




def recherche_salarie(request):
    query = request.GET.get('q', '')
    
    if query:
        salaries = Salaire.objects.filter(employe__nom__icontains=query)  # Filtrer par nom de l'employé
    else:
        salaries = Salaire.objects.all()  # Récupérer tous les salaires

    context = {
        'salaries': salaries,
        'query': query,
    }
    return render(request, 'salaire_templates/recherche_salarie.html', context)