from django.shortcuts import render

#La page d'accueil
def accueil(request):
    return render(request, 'accueil_template/home.html')