from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    
    
    # Route pour afficher la liste des employés
    path('list_employes/', views.afficher_employes, name='list_employes'),
    
    # Routes pour gérer les congés
    path('conges/', views.liste_conges, name='liste_conges'),  # Liste des congés
    path('conges/ajouter/', views.ajouter_conge, name='ajouter_conge'),  # Ajouter un congé
    path('conges/<int:conge_id>', views.details_conge, name='details_conge'),  # Détails d'un congé
]
