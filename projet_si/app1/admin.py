from django.contrib import admin

# Register your models here.
from .models import Service,Employe,Formation,Conge,Contrat,Salaire,OffreEmploi,Recrutement,Evaluation,Candidature
admin.site.register(Service)
admin.site.register(Employe)
admin.site.register(Formation)
admin.site.register(Contrat)
admin.site.register(Salaire)
admin.site.register(OffreEmploi)
admin.site.register(Recrutement)
admin.site.register(Evaluation)
admin.site.register(Candidature)
