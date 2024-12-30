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
    path('liste_conges', views.liste_conges, name='liste_conges'),  # Liste des congés
    path('conges/ajouter/', views.ajouter_conge, name='ajouter_conge'),  # Ajouter un congé
    path('conges/', views.recherche_conge, name='manage_conges'),
    path('conges/details', views.details_conge, name='details_conge'),  # Détails d'un congé
    path('conges/edit/<int:conge_id>/', views.modifie_conge, name='edit_conge'),
    path('conges/delete/<int:conge_id>/', views.supprime_conge, name='delete_conge'),
    path('conges/consult/<int:conge_id>/', views.consult_conge, name='consult_conge'),

    path('salarie/modifie/<int:salaire_id>/', views.modifie_salaire, name='edit_salaire'), 
    path('salarie/supprime/<int:salaire_id>/', views.supprime_salaire, name='delete_salaire'),  
    path('salarie/consult/<int:salaire_id>/', views.consult_salaire, name='consult_salaire'),
    path('salarie/', views.recherche_salarie, name='manage_salaries'),  
    path('afficher_salaire/<int:employe_id>/<int:annee>/<int:mois>/', views.afficher_salaire, name='afficher_salaire'),
    path('fiche_de_paie/<int:employe_id>/<int:annee>/<int:mois>/', views.generer_fiche_de_paie, name='generer_fiche_de_paie'),
    path('afficher_salaire_tous_employes/tous/', views.afficher_salaire_tous_employes, name='afficher_salaire_tous_employes'),
    path('ajouter_salaire/', views.ajouter_salaire, name='ajouter_salaire'),
    path('ajouter_prime/', views.ajouter_prime, name='ajouter_prime'),
    path('ajouter_absence/', views.ajouter_absence, name='ajouter_absence'),
    path('afficher_primes/', views.afficher_primes, name='afficher_primes'),
    path('afficher_absences/', views.afficher_absences, name='afficher_absences'),
    path('contrats/', views.liste_contrats, name='liste_contrats'),
    path('contrats/ajouter/', views.ajouter_contrat, name='ajouter_contrat'),
    path('contrats/<int:contrat_id>/', views.details_contrat, name='details_contrat'),
    path('contrat/edit/<int:contrat_id>/', views.modifier_contrat, name='edit_contrat'),
    path('contrat/delete/<int:contrat_id>/', views.supprimer_contrat, name='delete_contrat'),
    path('contrats/<int:contrat_id>/modifier/', views.modifier_contrat, name='modifier_contrat'),
    path('contrats/<int:contrat_id>/supprimer/', views.supprimer_contrat, name='supprimer_contrat'),
    path('jobs/', views.job_offer_list, name='job_offer_list'),
    path('jobs/new/', views.job_offer_create, name='job_offer_create'),
    path('candidates/', views.candidate_list, name='candidate_list'),
    path('candidates/<int:candidate_id>/schedule/', views.interview_schedule, name='interview_schedule'),
   
    path('service/insert/', views.insert_service, name='insert_service'),
    path('service/edit/<int:service_id>/', views.modifie_service, name='edit_service'),
    path('service/delete/<int:service_id>/', views.supprime_service, name='delete_service'),
    path('service/consult/<int:service_id>/', views.consult_service, name='consult_service'),


    path('evaluation/ajouter/', views.ajouter_evaluation, name='ajouter_evaluation'),  # Ajouter une évaluation
    path('evaluations/', views.liste_evaluations, name='liste_evaluations'),  # Liste des évaluations
    path('evaluation/modifier/<int:evaluation_id>/', views.modifier_evaluation, name='modifier_evaluation'),  # Modifier une évaluation
    path('evaluation/supprimer/<int:evaluation_id>/', views.supprimer_evaluation, name='supprimer_evaluation'),  # Supprimer une évaluation
    

]
