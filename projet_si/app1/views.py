from datetime import date, datetime, timedelta
from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count, F
from .forms import AbsenceForm, ApplicationForm, CongeForm, ContratForm, DateRangeForm, EmployeForm, EvaluationForm, JobOfferForm, MasroufForm, PrimeForm, SalaireForm, ServiceForm
from .models import Absence, Application, Contrat, Employe, Conge, Evaluation, Interview, JobOffer, Masrouf, Prime, Salaire, Service


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
                
                return redirect('recherche_conge')
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

def details_conge(request,conge_id):
    """
    Affiche les détails d'un congé spécifique.
    """
    conge = get_object_or_404(Conge,id=conge_id)
    return render(request, 'details_conge.html', {'conge': conge})



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
    return render(request, 'gestion_salaire.html', context)


def ajouter_salaire(request):
    if request.method == "POST":
        form = SalaireForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_salaire')
    else:
        form = SalaireForm()
    return render(request, 'ajouter_salaire.html', {'form': form})





def modifier_salaire(request, salaire_id):
    salaire = get_object_or_404(Salaire, id=salaire_id)
    if request.method == "POST":
        form = SalaireForm(request.POST, instance=salaire)
        if form.is_valid():
            form.save()
            return redirect('gestion_salaire')
    else:
        form = SalaireForm(instance=salaire)
    return render(request, 'modifier_salaire.html', {'form': form})





def supprimer_salaire(request, salaire_id):
    salaire = get_object_or_404(Salaire, id=salaire_id)
    if request.method == "POST":
        salaire.delete()
        return redirect('gestion_salaire')
    return render(request, 'supprimer_salaire.html', {'salaire': salaire})


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
    return render(request, 'consulter_salaire.html', context)




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


# Gestion des absences
def gestion_absence(request):
    employes = Employe.objects.all()
    absences = Absence.objects.select_related('employe').all()

    if 'search' in request.GET:
        search_query = request.GET['search']
        absences = absences.filter(employe__nom__icontains=search_query)

    context = {
        'employes': employes,
        'absences': absences,
    }
    return render(request, 'gestion_absence.html', context)


def ajouter_absence(request):
    if request.method == 'POST':
        form = AbsenceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_absence')
    else:
        form = AbsenceForm()
    return render(request, 'ajouter_absence.html', {'form': form})

# Vue pour afficher les absences d'un employé
def afficher_absences(request):
    absences = Conge.objects.all()  # Récupère toutes les absences
    return render(request, 'afficher_absences.html', {'absences': absences})


def supprimer_absence(request, pk):
    absence = get_object_or_404(Absence, pk=pk)
    absence.delete()
    return redirect('gestion_absence')


def modifier_absence(request, pk):
    absence = get_object_or_404(Absence, pk=pk)
    if request.method == 'POST':
        form = AbsenceForm(request.POST, instance=absence)
        if form.is_valid():
            form.save()
            return redirect('gestion_absence')
    else:
        form = AbsenceForm(instance=absence)
    return render(request, 'modifier_absence.html', {'form': form})


def consulter_absences(request):
    query = request.GET.get('q', '')
    absences = Absence.objects.all()
    if query:
        absences = absences.filter(employe__nom__icontains=query)

    context = {
        'absences': absences,
        'query': query
    }
    return render(request, 'consulter_absences.html', context)



def ajouter_prime(request):
    if request.method == 'POST':
        form = PrimeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_prime')
    else:
        form = PrimeForm()
    return render(request, 'ajouter_prime.html', {'form': form})

# Vue pour afficher les primes d'un employé
def afficher_primes(request):
    primes = Prime.objects.all()  # Récupère toutes les primes
    return render(request, 'afficher_primes.html', {'primes': primes})

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
    return render(request, 'gestion_prime.html', context)


def supprimer_prime(request, pk):
    prime = get_object_or_404(Prime, pk=pk)
    prime.delete()
    return redirect('gestion_prime')


def modifier_prime(request, pk):
    prime = get_object_or_404(Prime, pk=pk)
    if request.method == 'POST':
        form = PrimeForm(request.POST, instance=prime)
        if form.is_valid():
            form.save()
            return redirect('gestion_prime')
    else:
        form = PrimeForm(instance=prime)
    return render(request, 'modifier_prime.html', {'form': form})


def consulter_primes(request):
    query = request.GET.get('q', '')
    primes = Prime.objects.all()
    if query:
        primes = primes.filter(employe__nom__icontains=query)

    context = {
        'primes': primes,
        'query': query
    }
    return render(request, 'consulter_primes.html', context)



def ajouter_contrat(request):
    if request.method == 'POST':
        form = ContratForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recherche_contrats')
    else:
        form = ContratForm()
    return render(request, 'ajouter_contrat.html', {'form': form})


def details_contrat(request, contrat_id):
    contrat = get_object_or_404(Contrat, id=contrat_id)
    return render(request, 'details_contrat.html', {'contrat': contrat})


def modifier_contrat(request, contrat_id):
    contrat = get_object_or_404(Contrat, id=contrat_id)
    if request.method == 'POST':
        form = ContratForm(request.POST, instance=contrat)
        if form.is_valid():
            form.save()
            return redirect('recherche_contrats')
    else:
        form = ContratForm(instance=contrat)
    return render(request, 'modifier_contrat.html', {'form': form})



  

def supprimer_contrat(request, contrat_id):
    contrat = get_object_or_404(Contrat, id=contrat_id)
    if request.method == 'POST':
        contrat.delete()  # Supprimer le congé
        return redirect('recherche_contrats')  # Rediriger vers la liste des congés
    context = {
        'contrat': contrat,
    }
    return render(request, 'supprimer_contrat.html', context)


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
    return render(request, 'recherche_contrats.html', context)


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


def create_job_offer(request):
    if request.method == 'POST':
        form = JobOfferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_offers_list')
    else:
        form = JobOfferForm()
    return render(request, 'create_job_offer.html', {'form': form})

def job_offers_list(request):
    job_offers = JobOffer.objects.all()
    return render(request, 'job_offers_list.html', {'job_offers': job_offers})

def apply_for_job(request, job_offer_id):
    job_offer = JobOffer.objects.get(id=job_offer_id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job_offer = job_offer
            application.save()
            return redirect('application_status', application_id=application.id)
    else:
        form = ApplicationForm()
    return render(request, 'apply_for_job.html', {'form': form, 'job_offer': job_offer})

def application_status(request, application_id):
    application = Application.objects.get(id=application_id)
    return render(request, 'application_status.html', {'application': application})

def schedule_interview(request, application_id):
    application = Application.objects.get(id=application_id)
    if request.method == 'POST':
        interview_date = request.POST['interview_date']
        location = request.POST['location']
        interviewer = request.POST['interviewer']
        interview = Interview.objects.create(
            application=application, 
            interview_date=interview_date, 
            location=location, 
            interviewer=interviewer
        )
        return redirect('interview_details', interview_id=interview.id)
    return render(request, 'schedule_interview.html', {'application': application})

def interview_details(request, interview_id):
    interview = Interview.objects.get(id=interview_id)

    if request.method == 'POST':
        status = request.POST.get('status')
        if status == 'Accepted':
            interview.application.status = 'accepted'  # Modifier le statut de l'application
        elif status == 'Rejected':
            interview.application.status = 'rejected'  # Modifier le statut de l'application
        interview.application.save()  # Sauvegarder les modifications du statut de l'application

        return redirect('interview_details', interview_id=interview.id)  # Rediriger pour rafraîchir la page

    return render(request, 'interview_details.html', {'interview': interview})

# Vue pour gérer les évaluations
def gestion_evaluations(request):
    evaluations = Evaluation.objects.select_related('employe').all()  # Chargement des évaluations avec les employés

    if 'search' in request.GET:
        search_query = request.GET['search']
        evaluations = evaluations.filter(employe__nom__icontains=search_query)

    context = {
        'evaluations': evaluations,
    }
    return render(request, 'gestion_evaluations.html', context)

# Vue pour ajouter une évaluation
def ajouter_evaluation(request):
    if request.method == 'POST':
        form = EvaluationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_evaluations')  # Redirige vers la gestion des évaluations
    else:
        form = EvaluationForm()
    return render(request, 'ajouter_evaluation.html', {'form': form})

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
    return render(request, 'modifier_evaluation.html', {'form': form})

# Vue pour supprimer une évaluation
def supprimer_evaluation(request, pk):
    evaluation = get_object_or_404(Evaluation, pk=pk)
    if request.method == 'POST':
        evaluation.delete()
        return redirect('gestion_evaluations')
    return render(request, 'supprimer_evaluation.html', {'evaluation': evaluation})

# Vue pour consulter une évaluation
def consulter_evaluation(request, pk):
    evaluation = get_object_or_404(Evaluation, pk=pk)
    return render(request, 'consulter_evaluation.html', {'evaluation': evaluation})


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
    return render(request, 'gestion_masrouf.html', context)


# Ajouter, modifier et supprimer des entités
def ajouter_masrouf(request):
    if request.method == 'POST':
        form = MasroufForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_masrouf')
    else:
        form = MasroufForm()
    return render(request, 'ajouter_masrouf.html', {'form': form})


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
    return render(request, 'modifier_masrouf.html', {'form': form})    


def consulter_masroufs(request):
    query = request.GET.get('q', '')
    masroufs = Masrouf.objects.all()
    if query:
        masroufs = masroufs.filter(employe__nom__icontains=query)

    context = {
        'masroufs': masroufs,
        'query': query
    }
    return render(request, 'consult_masroufs.html', context)


from .models import Employe, Evaluation
from .forms import EvaluationForm

def employe_evaluation(request, employee_id):
    employee = get_object_or_404(Employe, id=employee_id)
    evaluations = employee.evaluations.all()
    return render(request, 'employe_evaluation.html', {'employee': employee, 'evaluations': evaluations})

def evaluation_create(request, employee_id):
    employee = get_object_or_404(Employe, id=employee_id)
    if request.method == 'POST':
        form = EvaluationForm(request.POST)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.employe = employee
            evaluation.save()
            return redirect('employe_evaluation', employee_id=employee.id)
    else:
        form = EvaluationForm()
    return render(request, 'evaluation_form.html', {'form': form, 'employe': employee})




def analyse_effectifs(request):
    # Récupérer le filtre du type de contrat depuis la requête GET
    contrat_filtre = request.GET.get('type_contrat', '')

    # Si un filtre est appliqué, filtrer les contrats par type
    if contrat_filtre:
        contrats = Contrat.objects.filter(type_contrat=contrat_filtre)
    else:
        contrats = Contrat.objects.all()

    # Calculer le nombre total d'employés distincts
    total_employes = contrats.values('employe').distinct().count()

    # Récupérer les types de contrat pour le filtre
    types_contrat = Contrat._meta.get_field('type_contrat').choices

    context = {
        'contrats': contrats,
        'total_employes': total_employes,
        'contrat_filtre': contrat_filtre,
        'types_contrat': types_contrat,
    }
    return render(request, 'analyse_effectifs.html', context)





def repartition_employes(request):
    # Calculer la répartition par sexe
    sexe_counts = Employe.objects.values('sexe').annotate(count=Count('sexe'))
    sexe_labels = [sexe['sexe'] for sexe in sexe_counts]
    sexe_data = [sexe['count'] for sexe in sexe_counts]

    # Calculer la répartition par âge
    today = date.today()
    age_counts = Employe.objects.all()
    age_data = []
    for employe in age_counts:
        age = today.year - employe.date_naissance.year
        age_data.append(age)
    
    # Calculer la répartition par ancienneté
    anciennete_counts = Employe.objects.all()
    anciennete_data = []
    for employe in anciennete_counts:
        anciennete = today.year - employe.date_embauche.year
        anciennete_data.append(anciennete)

    context = {
        'sexe_labels': sexe_labels,
        'sexe_data': sexe_data,
        'age_data': age_data,
        'anciennete_data': anciennete_data,
    }
    return render(request, 'repartition_employes.html', context)







def top_performeurs(request):
    form = DateRangeForm(request.GET)
    start_date = None
    end_date = None

    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')

    if start_date and end_date:
        # Filtrer les évaluations par la période donnée
        top_evaluations = Evaluation.objects.filter(date_evaluation__range=[start_date, end_date]) \
                                             .order_by('-score')[:10]
    else:
        # Récupérer les 10 meilleures évaluations sans filtre de date
        top_evaluations = Evaluation.objects.all().order_by('-score')[:10]

    return render(request, 'top_performeurs.html', {'top_evaluations': top_evaluations, 'form': form})



from django.db.models.functions import TruncMonth


def analyse_activite(request):
    # Récupérer le mois choisi ou la date actuelle
    mois_choisi = request.GET.get('mois', datetime.now().strftime('%Y-%m'))  # Par défaut, mois courant

    # Convertir le mois choisi en format date (1er jour du mois)
    mois_choisi_date = datetime.strptime(mois_choisi, '%Y-%m')

    # Filtrer les absences par mois
    absences_par_mois = Absence.objects.annotate(
        mois=TruncMonth('date_absence')  # Truncation du champ date_absence pour obtenir le mois
    ).filter(
        mois__gte=mois_choisi_date, 
        mois__lt=mois_choisi_date.replace(day=28) + timedelta(days=4)  # Limiter à la période du mois
    ).values('mois').annotate(
        nombre_absences=Count('id')  # Nombre d'absences pour chaque mois
    ).order_by('mois')  # Tri par mois

    # Préparer les données pour le graphique
    mois = [absence['mois'].strftime('%Y-%m') for absence in absences_par_mois]  # Format du mois en 'YYYY-MM'
    nombre_absences = [absence['nombre_absences'] for absence in absences_par_mois]  # Compter les absences

    # Calculer un seuil pour identifier les pics d'absentéisme
    seuil = max(nombre_absences) * 0.75 if nombre_absences else 0  # Seuil des pics d'absentéisme

    return render(request, 'analyse_activite.html', {
        'mois': mois,
        'nombre_absences': nombre_absences,
        'seuil': seuil,
        'mois_choisi': mois_choisi,  # Passer le mois choisi au template
    })






