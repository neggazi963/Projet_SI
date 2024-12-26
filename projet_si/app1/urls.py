from django.contrib import admin

from django.urls import path,include

from . import views


from django.urls import path, include
urlpatterns = [ 
  path('app1/', include('app1.urls')),
  path('admin/', admin.site.urls),  # Django admin site URL
  path('', views.home, name='home'),  # Default URL for the application
  path('list_employes/',views.afficher_employes),
  path('conges/', views.liste_conges, name='liste_conges'),
  path('conges/ajouter/', views.ajouter_conge, name='ajouter_conge'),
  path('conges/<int:conge_id>/', views.details_conge, name='details_conge'),
]