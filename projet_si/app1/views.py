from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from .forms import AbsenceForm, CongeForm, ContratForm, InterviewForm, JobOfferForm, PrimeForm, SalaireForm
from .models import Absence, Candidate, Contrat, Employe, Conge, OffreEmploi, Prime

from django.http import JsonResponse
from django.db.models import Sum
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
    return render(request, 'rechercher_employe.html', context)


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
    return render(request, 'insert_employe.html', context)





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
    return render(request, 'modifie_employe.html', context)



def supprimer_employe(request, employe_id):
    employe = get_object_or_404(Employe, id=employe_id)

    if request.method == 'POST':
        employe.delete()  
        return redirect('rechercher_employe')  # Rediriger vers la liste des employés

    context = {
        'employe': employe,
    }
    return render(request, 'supprime_employe.html', context)



def consult_employe(request, employe_id):
    employe = get_object_or_404(Employe, id=employe_id)  

    context = {
        'employe': employe,
    }
    return render(request, 'consult_employe.html', context)
def afficher_employes(request):
   employes = Employe.objects.all()
   return render(request, "list_employes.html", {"employes": employes})  # Remplacé 'Employes' par 'employes'


def liste_conges(request):
    """
    Affiche la liste de tous les congés.
    Seuls les utilisateurs connectés peuvent accéder à cette vue.
    """
    conges = Conge.objects.all().select_related('employe', 'employe__service')
    return render(request, 'liste_conges.html', {'conges': conges})


def ajouter_conge(request):
    """
    Permet d'ajouter un nouveau congé.
    Accessible uniquement aux utilisateurs connectés.
    """
    if request.method == 'POST':
        form = CongeForm(request.POST)
        if form.is_valid():
            conge = form.save(commit=False)
            # Ajout d'une validation personnalisée ou autres traitements si nécessaires
            if conge.date_debut > conge.date_fin:
                messages.error(request, "La date de début ne peut pas être après la date de fin.")
            else:
                conge.save()
                
                return redirect('liste_conges')
    else:
        form = CongeForm()
    return render(request, 'ajouter_conge.html', {'form': form})

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
    return render(request, 'modifie_conge.html', context)
def supprime_conge(request, conge_id):
    conge = get_object_or_404(Conge, id=conge_id)

    if request.method == 'POST':
        conge.delete()  # Supprimer le congé
        return redirect('recherche_conge')  # Rediriger vers la liste des congés

    context = {
        'conge': conge,
    }
    return render(request, 'supprime_conge.html', context)
def consult_conge(request, conge_id):
    conge = get_object_or_404(Conge, id=conge_id)

    context = {
        'conge': conge,
    }
    return render(request, 'consult_conge.html', context)
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
    return render(request, 'recherche_conge.html', context)

def details_conge(request):
    """
    Affiche les détails d'un congé spécifique.
    """
    conge = get_object_or_404(Conge)
    return render(request, 'details_conge.html', {'conge': conge})



def calculer_salaire_total(employe, annee, mois):
    salaire_base = 30000  # Salaire de base par défaut
    salaire_journalier = Contrat.salaire_quotidien 

    # Récupérer les absences et primes pour ce mois
    absences = Absence.objects.filter(employe=employe, date_absence__year=annee, date_absence__month=mois)
    primes = Prime.objects.filter(employe=employe, date_prime__year=annee, date_prime__month=mois)

    # Calcul des absences
    total_absences = absences.count()
    impact_absences = total_absences * salaire_journalier

    # Calcul des primes
    primes_fixes = primes.filter(type_prime='fixe').aggregate(Sum('montant'))['montant__sum'] or 0
    primes_pourcentage = primes.filter(type_prime='pourcentage').aggregate(Sum('montant'))['montant__sum'] or 0
    primes_pourcentage_valeur = (primes_pourcentage / 100) * salaire_base
    total_primes = primes_fixes + primes_pourcentage_valeur

    # Calcul du salaire net
    salaire_net = salaire_base + total_primes - impact_absences
    return salaire_net



def ajouter_salaire(request):
    if request.method == 'POST':
        form = SalaireForm(request.POST)
        if form.is_valid():
            form.save()  # Enregistrer le salaire dans la base de données
            return redirect('afficher_salaire_tous_employes')  # Rediriger vers la page des salaires
    else:
        form = SalaireForm()  # Créer un formulaire vide pour GET

    return render(request, 'ajouter_salaire.html', {'form': form})

# Vue pour afficher le salaire d'un employé
def afficher_salaire(request, employe_id, annee, mois):
    employe = get_object_or_404(Employe, id=employe_id)
    salaire_net = calculer_salaire_total(employe, annee, mois)

    # Récupérer les primes et absences
    primes = Prime.objects.filter(employe=employe, date_prime__year=annee, date_prime__month=mois)
    absences = Absence.objects.filter(employe=employe, date_absence__year=annee, date_absence__month=mois)
    
    return render(request, 'afficher_salaire.html', {'employe': employe, 'salaire_net': salaire_net, 'annee': annee, 'mois': mois, 'primes': primes, 'absences': absences})
def modifie_salaire(request, salaire_id):
    salaire = get_object_or_404(Salaire, id=salaire_id)

    if request.method == 'POST':
        form = SalaireForm(request.POST, instance=salaire)
        if form.is_valid():
            form.save()  # Enregistrer les modifications
            return redirect('recherche_salarie')  # Rediriger vers la liste des salaires
    else:
        form = SalaireForm(instance=salaire)

    context = {
        'form': form,
        'salaire': salaire,
    }
    return render(request, 'modifie_salaire.html', context)





def supprime_salaire(request, salaire_id):
    salaire = get_object_or_404(Salaire, id=salaire_id)

    if request.method == 'POST':
        salaire.delete()  # Supprimer le salaire
        return redirect('rcherche_salarie')  # Rediriger vers la liste des salaires

    context = {
        'salaire': salaire,
    }
    return render(request, 'supprime_salaire.html', context)


def consult_salaire(request, salaire_id):
    salaire = get_object_or_404(Salaire, id=salaire_id)

    context = {
        'salaire': salaire,
    }
    return render(request, 'consult_salaire.html', context)


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
    return render(request, 'recherche_salarie.html', context)

def ajouter_absence(request):
    if request.method == 'POST':
        form = AbsenceForm(request.POST)
        if form.is_valid():
            form.save()  # Enregistrer l'absence dans la base de données
            return redirect('afficher_absences')  # Rediriger vers la page des absences
    else:
        form = AbsenceForm()  # Créer un formulaire vide pour GET

    return render(request, 'ajouter_absence.html', {'form': form})

# Vue pour afficher les absences d'un employé
def afficher_absences(request):
    absences = Conge.objects.all()  # Récupère toutes les absences
    return render(request, 'afficher_absences.html', {'absences': absences})

def ajouter_prime(request):
    if request.method == 'POST':
        form = PrimeForm(request.POST)
        if form.is_valid():
            form.save()  # Enregistrer la prime dans la base de données
            return redirect('afficher_primes')  # Rediriger vers la page des primes
    else:
        form = PrimeForm()  # Créer un formulaire vide pour GET

    return render(request, 'ajouter_prime.html', {'form': form})

# Vue pour afficher les primes d'un employé
def afficher_primes(request):
    primes = Prime.objects.all()  # Récupère toutes les primes
    return render(request, 'afficher_primes.html', {'primes': primes})

# Vue pour générer une fiche de paie numérique (au format JSON)
def generer_fiche_de_paie(request, employe_id, annee, mois):
    employe = get_object_or_404(Employe, id=employe_id)
    salaire_net = calculer_salaire_total(employe, annee, mois)
    absences = Absence.objects.filter(employe=employe, date_absence__year=annee, date_absence__month=mois)
    primes = Prime.objects.filter(employe=employe, date_prime__year=annee, date_prime__month=mois)
    
    fiche_de_paie = {
        'employe': {
            'nom': employe.nom,
            'prenom': employe.prenom,
            'poste': employe.service.nom_service if employe.service else 'Non défini'
        },
        'salaires': {
            'salaire_net': salaire_net,
            'salaire_base': 30000,
            'total_primes': sum([prime.montant for prime in primes]),
            'total_absences': sum([absence.impact_salaire for absence in absences]),
        },
        'absences': [{'date': absence.date_absence, 'raison': absence.raison, 'impact': absence.impact_salaire} for absence in absences],
        'primes': [{'date': prime.date_prime, 'montant': prime.montant, 'type': prime.type_prime} for prime in primes]
    }
    
    return JsonResponse(fiche_de_paie, safe=False)





def afficher_salaire_tous_employes(request):
    # Récupérer tous les employés
    employes = Employe.objects.all()
    salaires = []

    for employe in employes:
        # Salaire de base (fixé à 30 000 DA)
        salaire_base = 30000
        
        # Récupérer les primes de l'employé
        primes = Prime.objects.filter(employe=employe)
        total_primes = primes.aggregate(total=Sum('montant'))['total'] or 0
        
        # Récupérer les absences de l'employé et leur impact sur le salaire
        absences = Absence.objects.filter(employe=employe)
        total_absences = absences.aggregate(total=Sum('impact_salaire'))['total'] or 0
        
        # Salaire net calculé
        salaire_net = salaire_base + total_primes - total_absences

        # Ajouter les données à la liste des salaires
        salaires.append({
            'employe': employe,
            'salaire_base': salaire_base,
            'total_primes': total_primes,
            'total_absences': total_absences,
            'salaire_net': salaire_net
        })

    # Renvoyer les données au template
    return render(request, 'afficher_salaire_tous_employes.html', {'salaires': salaires})


def liste_contrats(request):
    contrats = Contrat.objects.filter(archived=False)
    return render(request, 'contrats/liste_contrats.html', {'contrats': contrats})


def ajouter_contrat(request):
    if request.method == 'POST':
        form = ContratForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_contrats')
    else:
        form = ContratForm()
    return render(request, 'contrats/ajouter_contrat.html', {'form': form})


def details_contrat(request, contrat_id):
    contrat = get_object_or_404(Contrat, id=contrat_id)
    return render(request, 'contrats/details_contrat.html', {'contrat': contrat})


def modifier_contrat(request, contrat_id):
    contrat = get_object_or_404(Contrat, id=contrat_id)
    if request.method == 'POST':
        form = ContratForm(request.POST, instance=contrat)
        if form.is_valid():
            form.save()
            return redirect('liste_contrats')
    else:
        form = ContratForm(instance=contrat)
    return render(request, 'contrats/modifier_contrat.html', {'form': form})


def supprimer_contrat(request, contrat_id):
    contrat = get_object_or_404(Contrat, id=contrat_id)
    contrat.archived = True
    contrat.save()
    return redirect('liste_contrats')
def consult_contrat(request, contrat_id):
    contrat = get_object_or_404(Contrat, id=contrat_id)

    context = {
        'contrat': contrat,
    }
    return render(request, 'consult_contrat.html', context)

def gerer_contrats(request):
    
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
    return render(request, 'gerer_contrat.html', context)


def insert_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()  # Enregistrer le nouveau service
            return redirect('recherche_service')  # Rediriger vers la liste des services
    else:
        form = ServiceForm()

    context = {
        'form': form,
    }
    return render(request, 'insert_service.html', context)





def modifie_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()  # Enregistrer les modifications
            return redirect('recherche_service.html')  # Rediriger vers la liste des services
    else:
        form = ServiceForm(instance=service)

    context = {
        'form': form,
        'service': service,
    }
    return render(request, 'modifie_service.html', context)



def supprime_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        service.delete()  # Supprimer le service
        return redirect('recherche_service.html')  # Rediriger vers la liste des services

    context = {
        'service': service,
    }
    return render(request, 'supprime_service.html', context)


def rechercher_service(request):
    query = request.GET.get('q', '')
    
    if query:
        services = Service.objects.filter(nom_service__icontains=query)  # Filtrer par nom de service
    else:
        services = Service.objects.all()  # Récupérer tous les services

    context = {
        'services': services,
        'query': query,
    }
    return render(request, 'recherche_service.html', context)



def consult_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    context = {
        'service': service,
    }
    return render(request, 'consult_service.html', context)


def job_offer_list(request):
    offers = OffreEmploi.objects.all()
    return render(request, 'recruitment/job_offer_list.html', {'offers': offers})

def job_offer_create(request):
    if request.method == 'POST':
        form = OffreEmploi(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_offer_list')
    else:
        form = JobOfferForm()
    return render(request, 'recruitment/job_offer_create.html', {'form': form})

def candidate_list(request):
    candidates = Candidate.objects.all()
    return render(request, 'recruitment/candidate_list.html', {'candidates': candidates})

def interview_schedule(request, candidate_id):
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.candidate = candidate
            interview.save()
            return redirect('candidate_list')
    else:
        form = InterviewForm()
    return render(request, 'recruitment/interview_schedule.html', {'form': form, 'candidate': candidate})