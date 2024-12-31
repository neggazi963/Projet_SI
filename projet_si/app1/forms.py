from django import forms
from .models import Absence, Candidat, Conge, Contrat, Employe, Evaluation, OffreEmploi, Prime, Salaire, Service


class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = "__all__"


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = "__all__"
        


class CongeForm(forms.ModelForm):
    class Meta:
        model = Conge
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get("date_debut")
        date_fin = cleaned_data.get("date_fin")

        # Vérification que la date de début est avant la date de fin
        if date_debut and date_fin:
            if date_debut > date_fin:
                raise forms.ValidationError("La date de début ne peut pas être après la date de fin.")

        return cleaned_data
    

class SalaireForm(forms.ModelForm):
    class Meta:
        model = Salaire
        fields = "__all__"


class PrimeForm(forms.ModelForm):
    class Meta:
        model = Prime
        fields = "__all__"


class AbsenceForm(forms.ModelForm):
    class Meta:
        model = Absence
        fields = "__all__"

class ContratForm(forms.ModelForm):
    class Meta:
        model = Contrat
        fields = "__all__"



class CandidatureForm(forms.ModelForm):
    class Meta:
        model = Candidat
        fields = "__all__"

class OffreEmploiForm(forms.ModelForm):
    class Meta:
        model = OffreEmploi
        fields = "__all__"


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = "__all__"
        widgets = {
            'date_evaluation': forms.DateInput(attrs={'type': 'date'}),
        }      