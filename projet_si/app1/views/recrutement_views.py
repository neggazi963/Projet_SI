from django.shortcuts import redirect, render
from app1.forms import ApplicationForm, JobOfferForm
from app1.models import Application, Interview, JobOffer


def create_job_offer(request):
    if request.method == 'POST':
        form = JobOfferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_offers_list')
    else:
        form = JobOfferForm()
    return render(request, 'recrutement_templates/create_job_offer.html', {'form': form})

def job_offers_list(request):
    job_offers = JobOffer.objects.all()
    return render(request, 'recrutement_templates/job_offers_list.html', {'job_offers': job_offers})

def apply_for_job(request, job_offer_id):
    job_offer = JobOffer.objects.get(id=job_offer_id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job_offer = job_offer
            application.save()
            return redirect('application_status', application_id=application.id)
    else:
        form = ApplicationForm()
    return render(request, 'recrutement_templates/apply_for_job.html', {'form': form, 'job_offer': job_offer})

def application_status(request, application_id):
    application = Application.objects.get(id=application_id)
    return render(request, 'recrutement_templates/application_status.html', {'application': application})

def schedule_interview(request, application_id):
    application = Application.objects.get(id=application_id)
    if request.method == 'POST':
        interview_date = request.POST['interview_date']
        location = request.POST['location']
        interviewer = request.POST['interviewer']
        interview = Interview.objects.create(
            application=application, 
            interview_date=interview_date, 
            location=location, 
            interviewer=interviewer
        )
        return redirect('interview_details', interview_id=interview.id)
    return render(request, 'recrutement_templates/schedule_interview.html', {'application': application})

def interview_details(request, interview_id):
    interview = Interview.objects.get(id=interview_id)

    if request.method == 'POST':
        status = request.POST.get('status')
        if status == 'Accepted':
            interview.application.status = 'accepted'  # Modifier le statut de l'application
        elif status == 'Rejected':
            interview.application.status = 'rejected'  # Modifier le statut de l'application
        interview.application.save()  # Sauvegarder les modifications du statut de l'application

        return redirect('interview_details', interview_id=interview.id)  # Rediriger pour rafraîchir la page

    return render(request, 'recrutement_templates/interview_details.html', {'interview': interview})