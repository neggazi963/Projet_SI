from django.shortcuts import get_object_or_404, redirect, render

from app1.forms import ServiceForm
from app1.models import Service


def insert_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()  # Enregistrer le nouveau service
            return redirect('recherche_service')  # Rediriger vers la liste des services
    else:
        form = ServiceForm()

    context = {
        'form': form,
    }
    return render(request, 'service_templates/insert_service.html', context)





def modifie_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()  # Enregistrer les modifications
            return redirect('service_templates/recherche_service.html')  # Rediriger vers la liste des services
    else:
        form = ServiceForm(instance=service)

    context = {
        'form': form,
        'service': service,
    }
    return render(request, 'service_templates/modifie_service.html', context)



def supprime_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        service.delete()  # Supprimer le service
        return redirect('service_templates/recherche_service.html')  # Rediriger vers la liste des services

    context = {
        'service': service,
    }
    return render(request, 'service_templates/supprime_service.html', context)


def rechercher_service(request):
    query = request.GET.get('q', '')
    
    if query:
        services = Service.objects.filter(nom_service__icontains=query)  # Filtrer par nom de service
    else:
        services = Service.objects.all()  # Récupérer tous les services

    context = {
        'services': services,
        'query': query,
    }
    return render(request, 'service_templates/recherche_service.html', context)



def consult_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    context = {
        'service': service,
    }
    return render(request, 'service_templates/consult_service.html', context)