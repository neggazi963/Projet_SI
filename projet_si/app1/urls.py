from django.contrib import admin

from django.urls import path,include

from . import views



urlpatterns = [ 
   path('admin/', admin.site.urls),
   path('', include('app1.urls')),  
   path('list_employes/', views.afficher_employes, name='list_employes'),
  path('conges/', views.liste_conges, name='liste_conges'),
  path('conges/ajouter/', views.ajouter_conge, name='ajouter_conge'),
  path('conges/<int:conge_id>/', views.details_conge, name='details_conge'),
]