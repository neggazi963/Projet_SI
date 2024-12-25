from django.shortcuts import render 
from .models import Employe
def afficher_employes(request):
   employes = Employe.objects.all()
   return render(request,"index.html",{"Employes":employes})
