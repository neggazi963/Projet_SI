from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    
    
    # Route pour afficher la liste des employés
    path('list_employes/', views.afficher_employes, name='list_employes'),
    
    # Routes pour gérer les congés
    path('liste_conges', views.liste_conges, name='liste_conges'),  # Liste des congés
    path('conges/ajouter/', views.ajouter_conge, name='ajouter_conge'),  # Ajouter un congé
    path('details_conge/<int:conge_id>/', views.details_conge, name='details_conge'),  # Détails d'un congé
    path('afficher_salaire/<int:employe_id>/<int:annee>/<int:mois>/', views.afficher_salaire, name='afficher_salaire'),
    path('fiche_de_paie/<int:employe_id>/<int:annee>/<int:mois>/', views.generer_fiche_de_paie, name='generer_fiche_de_paie'),
    path('afficher_salaire_tous_employes/tous/', views.afficher_salaire_tous_employes, name='afficher_salaire_tous_employes'),
    path('ajouter_salaire/', views.ajouter_salaire, name='ajouter_salaire'),
    path('ajouter_prime/', views.ajouter_prime, name='ajouter_prime'),
    path('ajouter_absence/', views.ajouter_absence, name='ajouter_absence'),
    path('afficher_primes/', views.afficher_primes, name='afficher_primes'),
    path('afficher_absences/', views.afficher_absences, name='afficher_absences'),
]
