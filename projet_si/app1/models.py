from django.db import models

class Service(models.Model):
    id_service = models.AutoField(primary_key=True)
    description = models.TextField()

    def __str__(self):
        return f"Service {self.id_service}: {self.description}"

class Employe(models.Model):
    id_employe = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    date_embauche = models.DateField()
    adresse = models.TextField()
    id_service = models.ForeignKey(Service, on_delete=models.CASCADE)
    competences = models.TextField()
    historique_professionnel = models.TextField()

    def __str__(self):
        return f"Employe {self.nom} {self.prenom}"

class Formation(models.Model):
    id_formation = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    description = models.TextField()
    employes = models.ManyToManyField(Employe, related_name='formations')

    def __str__(self):
        return self.nom

class Conge(models.Model):
    id_conge = models.AutoField(primary_key=True)
    id_employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()
    type_conge = models.CharField(max_length=50)

    def __str__(self):
        return f"Conge {self.id_conge} ({self.type_conge})"

class Contrat(models.Model):
    id_contrat = models.AutoField(primary_key=True)
    id_employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    type_contrat = models.CharField(max_length=50)
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    salaire_mensuel = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salaire_quotidien = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Contrat {self.type_contrat} pour {self.id_employe.nom}"

class Salaire(models.Model):
    id_salaire = models.AutoField(primary_key=True)
    id_employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateField()

    def __str__(self):
        return f"Salaire de {self.montant} pour {self.id_employe.nom}"

class OffreEmploi(models.Model):
    id_offre = models.AutoField(primary_key=True)
    titre_offre = models.CharField(max_length=100)
    description = models.TextField()
    date_publication = models.DateField()
    statut = models.CharField(max_length=50)

    def __str__(self):
        return self.titre_offre

class Recrutement(models.Model):
    id_recrutement = models.AutoField(primary_key=True)
    id_offre = models.ForeignKey(OffreEmploi, on_delete=models.CASCADE)
    id_employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    date_recrutement = models.DateField()
    statut = models.CharField(max_length=50)

    def __str__(self):
        return f"Recrutement pour {self.id_offre.titre_offre}"

class Evaluation(models.Model):
    id_evaluation = models.AutoField(primary_key=True)
    id_employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    date_evaluation = models.DateField()
    score = models.IntegerField()
    commentaires = models.TextField()

    def __str__(self):
        return f"Evaluation de {self.id_employe.nom}"

class Candidature(models.Model):
    id_candidature = models.AutoField(primary_key=True)
    id_offre = models.ForeignKey(OffreEmploi, on_delete=models.CASCADE)
    id_candidat = models.ForeignKey(Employe, on_delete=models.CASCADE)
    statut_candidature = models.CharField(max_length=50)

    def __str__(self):
        return f"Candidature {self.id_candidature} ({self.statut_candidature})"
