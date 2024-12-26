from django import forms
from .models import Conge

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
