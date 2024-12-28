from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    
    
    # Route pour afficher la liste des employés
    path('list_employes/', views.afficher_employes, name='list_employes'),
    
    # Routes pour gérer les congés
    path('liste_conges', views.liste_conges, name='liste_conges'),  # Liste des congés
    path('conges/ajouter/', views.ajouter_conge, name='ajouter_conge'),  # Ajouter un congé

    path('conges/details', views.details_conge, name='details_conge'),  # Détails d'un congé

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
    path('contrats/<int:contrat_id>/modifier/', views.modifier_contrat, name='modifier_contrat'),
    path('contrats/<int:contrat_id>/supprimer/', views.supprimer_contrat, name='supprimer_contrat'),
    path('jobs/', views.job_offer_list, name='job_offer_list'),
    path('jobs/new/', views.job_offer_create, name='job_offer_create'),
    path('candidates/', views.candidate_list, name='candidate_list'),
    path('candidates/<int:candidate_id>/schedule/', views.interview_schedule, name='interview_schedule'),

]
