from django.db import models

class Service(models.Model):
    description = models.TextField()

    def __str__(self):
        return f"Service {self.id}: {self.description}"

class Employe(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    date_embauche = models.DateField()
    adresse = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
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
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()
    type_conge = models.CharField(max_length=50)
    solde = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) 

    def __str__(self):
        return f"Congé {self.id} ({self.type_conge})"

class Contrat(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    type_conge = models.CharField(max_length=50)
    date_debut = models.DateField()
    date_fin = models.DateField()
    jours_utilises = models.PositiveIntegerField()
    solde_initial = models.PositiveIntegerField()
    solde_restant = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        self.jours_utilises = (self.date_fin - self.date_debut).days + 1
        self.solde_restant = self.solde_initial - self.jours_utilises
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employe.nom} - {self.type_conge.nom}"

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
        unique_together = ('offre', 'employe')

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
    statut_candidature = models.CharField(max_length=50)

    def __str__(self):
        return f"Candidature {self.id} ({self.statut_candidature})"
