
from django.urls import path




from app1 import views


from .views import employe_views, absence_views, analyse_views, conge_views, contrat_views, evaluation_views, masrouf_views, prime_views, recrutement_views, salaire_views, service_views


urlpatterns = [
    
    
    # Route pour afficher la liste des employés
    path('employe/recherche/', employe_views.rechercher_employe, name='manage_employe'),
    path('employe/insert/',employe_views.insert_employe, name='insert_employe'),
    path('employees/edit/<int:employe_id>/', employe_views.modifier_employe, name='edit_employe'),
    path('employees/delete/<int:employe_id>/', employe_views.supprimer_employe, name='delete_employe'),
    path('employees/consult/<int:employe_id>/', employe_views.consult_employe, name='consult_employe'),
    
    # Routes pour gérer les congés
    
    path('conges/ajouter/', conge_views.ajouter_conge, name='ajouter_conge'),  # Ajouter un congé
    path('conges/', conge_views.recherche_conge, name='recherche_conge'),
    path('conges/details/<int:conge_id>/', conge_views.details_conge, name='details_conge'),  # Détails d'un congé
    path('conges/edit/<int:conge_id>/', conge_views.modifie_conge, name='edit_conge'),
    path('conges/delete/<int:conge_id>/', conge_views.supprime_conge, name='delete_conge'),
    

    path('salaires/', salaire_views.gestion_salaire, name='gestion_salaire'),
    path('salaires/<int:employe_id>/consulter/', salaire_views.consulter_salaire, name='consulter_salaire'),
    path('salaires/ajouter/', salaire_views.ajouter_salaire, name='ajouter_salaire'),
    path('salaires/<int:salaire_id>/modifier/', salaire_views.modifier_salaire, name='modifier_salaire'),
    path('salaires/<int:salaire_id>/supprimer/', salaire_views.supprimer_salaire, name='supprimer_salaire'),
    
    path('ajouter/absence/', absence_views.ajouter_absence, name='ajouter_absence'),
    path('supprimer/absence/<int:pk>/', absence_views.supprimer_absence, name='supprimer_absence'),
    path('modifier/absence/<int:pk>/', absence_views.modifier_absence, name='modifier_absence'),
    path('consulter/absences/', absence_views.consulter_absences, name='consulter_absences'),
    path('gestion/absences/', absence_views.gestion_absence, name='gestion_absence'),

    path('ajouter/prime/', prime_views.ajouter_prime, name='ajouter_prime'),
    path('supprimer/prime/<int:pk>/', prime_views.supprimer_prime, name='supprimer_prime'),
    path('modifier/prime/<int:pk>/', prime_views.modifier_prime, name='modifier_prime'),
    path('consulter/primes/', prime_views.consulter_primes, name='consulter_primes'),
    path('gestion/primes/', prime_views.gestion_prime, name='gestion_prime'),

    path('ajouter/masrouf/', masrouf_views.ajouter_masrouf, name='ajouter_masrouf'),
    path('supprimer/masrouf/<int:pk>/', masrouf_views.supprimer_masrouf, name='supprimer_masrouf'),
    path('modifier/masrouf/<int:pk>/', masrouf_views.modifier_masrouf, name='modifier_masrouf'),
    path('gestion/masroufs/', masrouf_views.gestion_masrouf, name='gestion_masrouf'),

    path('contrats/', contrat_views.recherche_contrats, name='recherche_contrats'),
    path('contrats/ajouter/', contrat_views.ajouter_contrat, name='ajouter_contrat'),
    path('contrats/<int:contrat_id>/', contrat_views.details_contrat, name='details_contrat'),
    path('contrat/edit/<int:contrat_id>/', contrat_views.modifier_contrat, name='modifier_contrat'),
    path('contrat/delete/<int:contrat_id>/', contrat_views.supprimer_contrat, name='supprimer_contrat'),
    
    
    
    path('create-job-offer/', recrutement_views.create_job_offer, name='create_job_offer'),
    path('job-offers/', recrutement_views.job_offers_list, name='job_offers_list'),
    path('apply/<int:job_offer_id>/', recrutement_views.apply_for_job, name='apply_for_job'),
    path('application-status/<int:application_id>/', recrutement_views.application_status, name='application_status'),
    path('schedule-interview/<int:application_id>/', recrutement_views.schedule_interview, name='schedule_interview'),
    path('interview-details/<int:interview_id>/', recrutement_views.interview_details, name='interview_details'),

    path('service/insert/', service_views.insert_service, name='insert_service'),
    path('service/edit/<int:service_id>/', service_views.modifie_service, name='edit_service'),
    path('service/delete/<int:service_id>/', service_views.supprime_service, name='delete_service'),
    path('service/consult/<int:service_id>/', service_views.consult_service, name='consult_service'),


    path('evaluations/', evaluation_views.gestion_evaluations, name='gestion_evaluations'),
    path('evaluations/ajouter/', evaluation_views.ajouter_evaluation, name='ajouter_evaluation'),
    path('evaluations/modifier/<int:pk>/', evaluation_views.modifier_evaluation, name='modifier_evaluation'),
    path('evaluations/supprimer/<int:pk>/', evaluation_views.supprimer_evaluation, name='supprimer_evaluation'),
    path('evaluations/consulter/<int:pk>/', evaluation_views.consulter_evaluation, name='consulter_evaluation'),



    #path('employe/<int:employe_id>/evaluation/', views.employe_evaluation, name='employee_evaluations'),
    #path('employe/<int:employe_id>/evaluation/new/', views.evaluation_create, name='evaluation_create'),
    

   


    path('analyse_effectifs/', analyse_views.analyse_effectifs, name='analyse_effectifs'),
    path('repartition_employes/', analyse_views.repartition_employes, name='repartition_employes'),
    path('top-performeurs/', analyse_views.top_performeurs, name='top_performeurs'),
    path('analyse-activite/', analyse_views.analyse_activite, name='analyse_activite'),
]
