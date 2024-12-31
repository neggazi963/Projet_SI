from django.contrib import admin

# Register your models here.
from .models import Candidat, Service,Employe,Formation,Conge,Contrat,Salaire,OffreEmploi,Entretien,Evaluation,Absence,Prime
admin.site.register(Service)
admin.site.register(Employe)
admin.site.register(Formation)
admin.site.register(Contrat)
admin.site.register(Salaire)
admin.site.register(OffreEmploi)
admin.site.register(Entretien)
admin.site.register(Evaluation)
admin.site.register(Candidat)
admin.site.register(Conge)
admin.site.register(Absence)
admin.site.register(Prime)

