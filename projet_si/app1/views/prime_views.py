from django.shortcuts import get_object_or_404, redirect, render
from app1.forms import PrimeForm
from app1.models import Employe, Prime


#Gerer l'ajout d'une prime
def ajouter_prime(request):
    if request.method == 'POST':
        form = PrimeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_prime')
    else:
        form = PrimeForm()
    return render(request, 'prime_templates/ajouter_prime.html', {'form': form})


def afficher_primes(request):
    primes = Prime.objects.all()  # Récupère toutes les primes
    return render(request, 'prime_templates/afficher_primes.html', {'primes': primes})

# Gestion des primes
def gestion_prime(request):
    employes = Employe.objects.all()
    primes = Prime.objects.select_related('employe').all()

    if 'search' in request.GET:
        search_query = request.GET['search']
        primes = primes.filter(employe__nom__icontains=search_query)

    context = {
        'employes': employes,
        'primes': primes,
    }
    return render(request, 'prime_templates/gestion_prime.html', context)


#Gerer la suppression d'une prime
def supprimer_prime(request, pk):
    prime = get_object_or_404(Prime, pk=pk)
    prime.delete()
    return redirect('gestion_prime')


#Gerer la modification d'une prime
def modifier_prime(request, pk):
    prime = get_object_or_404(Prime, pk=pk)
    if request.method == 'POST':
        form = PrimeForm(request.POST, instance=prime)
        if form.is_valid():
            form.save()
            return redirect('gestion_prime')
    else:
        form = PrimeForm(instance=prime)
    return render(request, 'prime_templates/modifier_prime.html', {'form': form})


def consulter_primes(request):
    query = request.GET.get('q', '')
    primes = Prime.objects.all()
    if query:
        primes = primes.filter(employe__nom__icontains=query)

    context = {
        'primes': primes,
        'query': query
    }
    return render(request, 'prime_templates/consulter_primes.html', context)