from django.db import models
from django.urls import reverse

class Service(models.Model):
    nom_service = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return f"Service {self.id}: {self.nom_service}"

class Employe(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    date_embauche = models.DateField()
    adresse = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    competences = models.TextField()
    historique_professionnel = models.TextField()

    def __str__(self):
        return f"Employé {self.nom} {self.prenom}"

class Formation(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    employes = models.ManyToManyField(Employe, related_name='formations')

    def __str__(self):
        return self.nom

class Conge(models.Model):
    TYPE_CONGE_CHOICES = [
        ('Annuel', 'Congé Annuel'),
        ('Maladie', 'Congé Maladie'),
        ('Maternité', 'Congé Maternité/Paternité'),
        ('Sans Solde', 'Congé Sans Solde'),
    ]
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    type_conge = models.CharField(max_length=20, choices=TYPE_CONGE_CHOICES)
    date_debut = models.DateField()
    date_fin = models.DateField()
    jours_utilises = models.PositiveIntegerField(default=0)
    solde_initial = models.PositiveIntegerField()
    solde_restant = models.PositiveIntegerField(default=15)

    def save(self, *args, **kwargs):
        if self.date_debut and self.date_fin:
            self.jours_utilises = (self.date_fin - self.date_debut).days + 1
            self.solde_restant = self.solde_initial - self.jours_utilises
            if self.solde_restant < 0:
                self.solde_restant = 0  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employe.nom} - {self.type_conge}"

class Contrat(models.Model):
    employe = models.ForeignKey('Employe', on_delete=models.CASCADE)  # 'Employe' doit être défini dans le projet.
    type_contrat = models.CharField(max_length=50)  # Exemple : "CDI", "CDD", "Stage"
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    periode_essai = models.BooleanField(default=False)
    renouvellement = models.BooleanField(default=False)
    salaire_mensuel = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salaire_quotidien = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    archived = models.BooleanField(default=False)
    TYPE_CHOICES = [
    ('CDI', 'Contrat à Durée Indéterminée'),
    ('CDD', 'Contrat à Durée Déterminée'),
    ('Stage', 'Stage'),
    ('Autre', 'Autre'),
]
    type_contrat = models.CharField(max_length=50, choices=TYPE_CHOICES)
    def __str__(self):
        return f"Contrat {self.type_contrat} pour {self.employe.nom}"  # Assure que `Employe` a un champ `nom`.

    def get_absolute_url(self):
        return reverse('details_contrat', args=[self.id])  # URL dynamique pour accéder aux détails d'un contrat.
class Salaire(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateField()

    def __str__(self):
        return f"Salaire de {self.montant} pour {self.employe.nom}"

class OffreEmploi(models.Model):
    titre_offre = models.CharField(max_length=100)
    description = models.TextField()
    date_publication = models.DateField()
    statut = models.CharField(max_length=50)

    def __str__(self):
        return self.titre_offre

class Recrutement(models.Model):
    offre = models.ForeignKey(OffreEmploi, on_delete=models.CASCADE)
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    date_recrutement = models.DateField()
    statut = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['offre', 'employe'], name='unique_recrutement')
        ]

    def __str__(self):
        return f"Recrutement pour {self.offre.titre_offre} et {self.employe.nom}"

class Evaluation(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    date_evaluation = models.DateField()
    score = models.IntegerField()
    commentaires = models.TextField()

    def __str__(self):
        return f"Évaluation de {self.employe.nom}"

class Candidature(models.Model):
    offre = models.ForeignKey(OffreEmploi, on_delete=models.CASCADE)
    candidat = models.ForeignKey(Employe, on_delete=models.CASCADE)  

    def __str__(self):
        return f"Candidature {self.id} ({self.statut_candidature})"
    


class Absence(models.Model):
    employe = models.ForeignKey('Employe', on_delete=models.CASCADE)
    date_absence = models.DateField()
    raison = models.CharField(max_length=200, null=True, blank=True)
    impact_salaire = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Impact en DA

    def save(self, *args, **kwargs):
        salaire_journalier = 30000 / 30  # Salaire journalier par défaut
        self.impact_salaire = salaire_journalier  # Impact calculé automatiquement
        super().save(*args, **kwargs)


# Modèle Prime
class Prime(models.Model):
    employe = models.ForeignKey('Employe', on_delete=models.CASCADE)
    date_prime = models.DateField()
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    type_prime = models.CharField(max_length=50, choices=[('fixe', 'Fixe'), ('pourcentage', 'Pourcentage')])
    base_calcul = models.DecimalField(max_digits=10, decimal_places=2, default=30000)  # Salaire base utilisé

    def __str__(self):
        return f"Prime de {self.montant} pour {self.employe.nom}"   
         

class Candidate(models.Model):
    STATUS_CHOICES = [
        ('received', 'Reçue'),
        ('processing', 'En cours de traitement'),
        ('rejected', 'Rejetée'),
        ('accepted', 'Acceptée'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    offre  = models.ForeignKey(OffreEmploi, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='received')
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)

    def __str__(self):
        return self.name

class Interview(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    date = models.DateTimeField()
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Interview avec {self.candidate.name} le {self.date}"