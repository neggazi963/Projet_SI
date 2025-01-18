from datetime import date, datetime, timedelta
from django.db.models import Count
from app1.forms import DateRangeForm
from app1.models import Absence, Contrat, Employe, Evaluation
from django.db.models.functions import TruncMonth
from django.shortcuts import render



#Gerer l'analyse d'effectifs
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
    return render(request, 'analyse_templates/analyse_effectifs.html', context)




#gerer la repartition des employes 
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
    return render(request, 'analyse_templates/repartition_employes.html', context)






#Gerer les employes top performurs
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

    return render(request, 'analyse_templates/top_performeurs.html', {'top_evaluations': top_evaluations, 'form': form})





#Gerer l'analyse d'activité
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

    return render(request, 'analyse_templates/analyse_activite.html', {
        'mois': mois,
        'nombre_absences': nombre_absences,
        'seuil': seuil,
        'mois_choisi': mois_choisi,  # Passer le mois choisi au template
    })


def gestion_analyse(request):
    # Votre logique ici
    return render(request, 'analyse_templates/gestion_analyse.html')