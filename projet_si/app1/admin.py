from django.contrib import admin

# Register your models here.

from .models import JobOffer, Masrouf, Service,Employe,Formation,Conge,Contrat,Salaire,Interview,Application,Evaluation,Absence,Prime


admin.site.register(Service)
admin.site.register(Employe)
admin.site.register(Formation)
admin.site.register(Contrat)
admin.site.register(Salaire)
admin.site.register(Interview)
admin.site.register(Application)
admin.site.register(Evaluation)
admin.site.register(JobOffer)
admin.site.register(Conge)
admin.site.register(Absence)
admin.site.register(Prime)
admin.site.register(Masrouf)

