from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    
    
    # Route pour afficher la liste des employés
    path('employe/recherche/', views.rechercher_employe, name='manage_employe'),
    path('employe/insert/',views.insert_employe, name='insert_employe'),
    path('employees/edit/<int:employe_id>/', views.modifier_employe, name='edit_employe'),
    path('employees/delete/<int:employe_id>/', views.supprimer_employe, name='delete_employe'),
    path('employees/consult/<int:employe_id>/', views.consult_employe, name='consult_employe'),
    
    # Routes pour gérer les congés
    
    path('conges/ajouter/', views.ajouter_conge, name='ajouter_conge'),  # Ajouter un congé
    path('conges/', views.recherche_conge, name='recherche_conge'),
    path('conges/details/<int:conge_id>/', views.details_conge, name='details_conge'),  # Détails d'un congé
    path('conges/edit/<int:conge_id>/', views.modifie_conge, name='edit_conge'),
    path('conges/delete/<int:conge_id>/', views.supprime_conge, name='delete_conge'),
    

    path('salaires/', views.gestion_salaire, name='gestion_salaire'),
    path('salaires/<int:employe_id>/consulter/', views.consulter_salaire, name='consulter_salaire'),
    path('salaires/ajouter/', views.ajouter_salaire, name='ajouter_salaire'),
    path('salaires/<int:salaire_id>/modifier/', views.modifier_salaire, name='modifier_salaire'),
    path('salaires/<int:salaire_id>/supprimer/', views.supprimer_salaire, name='supprimer_salaire'),
    
    path('ajouter/absence/', views.ajouter_absence, name='ajouter_absence'),
    path('supprimer/absence/<int:pk>/', views.supprimer_absence, name='supprimer_absence'),
    path('modifier/absence/<int:pk>/', views.modifier_absence, name='modifier_absence'),
    path('consulter/absences/', views.consulter_absences, name='consulter_absences'),
    path('gestion/absences/', views.gestion_absence, name='gestion_absence'),

    path('ajouter/prime/', views.ajouter_prime, name='ajouter_prime'),
    path('supprimer/prime/<int:pk>/', views.supprimer_prime, name='supprimer_prime'),
    path('modifier/prime/<int:pk>/', views.modifier_prime, name='modifier_prime'),
    path('consulter/primes/', views.consulter_primes, name='consulter_primes'),
    path('gestion/primes/', views.gestion_prime, name='gestion_prime'),

    path('ajouter/masrouf/', views.ajouter_masrouf, name='ajouter_masrouf'),
    path('supprimer/masrouf/<int:pk>/', views.supprimer_masrouf, name='supprimer_masrouf'),
    path('modifier/masrouf/<int:pk>/', views.modifier_masrouf, name='modifier_masrouf'),
    path('gestion/masroufs/', views.gestion_masrouf, name='gestion_masrouf'),

    path('contrats/', views.recherche_contrats, name='recherche_contrats'),
    path('contrats/ajouter/', views.ajouter_contrat, name='ajouter_contrat'),
    path('contrats/<int:contrat_id>/', views.details_contrat, name='details_contrat'),
    path('contrat/edit/<int:contrat_id>/', views.modifier_contrat, name='modifier_contrat'),
    path('contrat/delete/<int:contrat_id>/', views.supprimer_contrat, name='supprimer_contrat'),
    
    
    
    path('create-job-offer/', views.create_job_offer, name='create_job_offer'),
    path('job-offers/', views.job_offers_list, name='job_offers_list'),
    path('apply/<int:job_offer_id>/', views.apply_for_job, name='apply_for_job'),
    path('application-status/<int:application_id>/', views.application_status, name='application_status'),
    path('schedule-interview/<int:application_id>/', views.schedule_interview, name='schedule_interview'),
    path('interview-details/<int:interview_id>/', views.interview_details, name='interview_details'),

    path('service/insert/', views.insert_service, name='insert_service'),
    path('service/edit/<int:service_id>/', views.modifie_service, name='edit_service'),
    path('service/delete/<int:service_id>/', views.supprime_service, name='delete_service'),
    path('service/consult/<int:service_id>/', views.consult_service, name='consult_service'),


    path('evaluations/', views.gestion_evaluations, name='gestion_evaluations'),
    path('evaluations/ajouter/', views.ajouter_evaluation, name='ajouter_evaluation'),
    path('evaluations/modifier/<int:pk>/', views.modifier_evaluation, name='modifier_evaluation'),
    path('evaluations/supprimer/<int:pk>/', views.supprimer_evaluation, name='supprimer_evaluation'),
    path('evaluations/consulter/<int:pk>/', views.consulter_evaluation, name='consulter_evaluation'),


    path('employe/<int:employe_id>/evaluation/', views.employe_evaluation, name='employee_evaluations'),
    path('employe/<int:employe_id>/evaluation/new/', views.evaluation_create, name='evaluation_create'),
]
