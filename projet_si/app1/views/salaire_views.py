from django.shortcuts import get_object_or_404, redirect, render
from app1.forms import SalaireForm
from app1.models import Absence, Employe, Masrouf, Prime, Salaire


def calculer_salaire(employe):
    salaire_base = 30000
    total_primes = Prime.objects.filter(employe=employe).aggregate(Sum('montant'))['montant__sum'] or 0
    total_absences = Absence.objects.filter(employe=employe).aggregate(Sum('impact_salaire'))['impact_salaire__sum'] or 0
    total_masrouf = Masrouf.objects.filter(employe=employe).aggregate(Sum('montant'))['montant__sum'] or 0
    return salaire_base + total_primes - total_absences - total_masrouf


def gestion_salaire(request):
    employes = Employe.objects.all()
    salaires = Salaire.objects.select_related('employe').all()

    if 'search' in request.GET:
        search_query = request.GET['search']
        salaires = salaires.filter(employe__nom__icontains=search_query)

    context = {
        'employes': employes,
        'salaires': salaires,
    }
    return render(request, 'salaire_templates/gestion_salaire.html', context)


def ajouter_salaire(request):
    if request.method == "POST":
        form = SalaireForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_salaire')
    else:
        form = SalaireForm()
    return render(request, 'salaire_templates/ajouter_salaire.html', {'form': form})





def modifier_salaire(request, salaire_id):
    salaire = get_object_or_404(Salaire, id=salaire_id)
    if request.method == "POST":
        form = SalaireForm(request.POST, instance=salaire)
        if form.is_valid():
            form.save()
            return redirect('gestion_salaire')
    else:
        form = SalaireForm(instance=salaire)
    return render(request, 'salaire_templates/modifier_salaire.html', {'form': form})





def supprimer_salaire(request, salaire_id):
    salaire = get_object_or_404(Salaire, id=salaire_id)
    if request.method == "POST":
        salaire.delete()
        return redirect('gestion_salaire')
    return render(request, 'salaire_templates/supprimer_salaire.html', {'salaire': salaire})



from django.shortcuts import get_object_or_404, render
from django.db.models import Sum

def consulter_salaire(request, salaire_id):
    # Récupérer le salaire via salaire_id
    salaire = get_object_or_404(Salaire, id=salaire_id)

    # Récupérer l'employé associé au salaire
    employe = salaire.employe

    # Récupérer les autres objets Salaire associés
    salaires = employe.salaire_set.all()

    # Calculer le total des primes
    total_primes = employe.prime_set.aggregate(total=Sum('montant'))['total'] or 0

    # Calculer l'impact total des absences
    total_absences = employe.absence_set.aggregate(total=Sum('impact_salaire'))['total'] or 0

    # Calculer le total des masroufs
    total_masrouf = employe.masrouf_set.aggregate(total=Sum('montant'))['total'] or 0

    context = {
        'employe': employe,
        'salaires': salaires,
        'total_primes': total_primes,
        'total_absences': total_absences,
        'total_masrouf': total_masrouf,
        'salaire_base': 30000,  # Salaire de base (exemple)
        'salaire_consulte': salaire,
    }
    return render(request, 'salaire_templates/consulter_salaire.html', context)





def recherche_salarie(request):
    query = request.GET.get('q', '')
    
    if query:
        salaries = Salaire.objects.filter(employe__nom__icontains=query)  # Filtrer par nom de l'employé
    else:
        salaries = Salaire.objects.all()  # Récupérer tous les salaires

    context = {
        'salaries': salaries,
        'query': query,
    }
    return render(request, 'salaire_templates/recherche_salarie.html', context)



from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def export_pdf(request, employe_id):
    employe = get_object_or_404(Employe, id=employe_id)
    salaires = employe.salaire_set.all()

    # Créer une réponse HTTP avec un contenu PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="salaires_{employe.nom}_{employe.prenom}.pdf"'

    # Générer le contenu PDF
    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, f"Salaires de {employe.nom} {employe.prenom}")

    # Ajouter les détails des salaires
    p.setFont("Helvetica", 12)
    y = 720
    p.drawString(100, y, f"Salaire de base: 30,000 DA")
    p.drawString(100, y - 20, f"Total des primes: {employe.prime_set.aggregate(total=Sum('montant'))['total'] or 0} DA")
    p.drawString(100, y - 40, f"Total des absences: {employe.absence_set.aggregate(total=Sum('impact_salaire'))['total'] or 0} DA")
    p.drawString(100, y - 60, f"Total Masrouf: {employe.masrouf_set.aggregate(total=Sum('montant'))['total'] or 0} DA")

    y -= 100
    p.drawString(100, y, "Détails des Salaires:")
    y -= 20

    if salaires.exists():
        for salaire in salaires:
            if y < 50:  # Vérifie si la page a assez d'espace
                p.showPage()
                p.setFont("Helvetica", 12)
                y = 750
            p.drawString(100, y, f"- Date: {salaire.date_paiement}, Montant: {salaire.montant} DA")
            y -= 20
    else:
        p.drawString(100, y, "Aucun salaire enregistré.")

    # Finaliser le PDF
    p.showPage()
    p.save()

    return response
