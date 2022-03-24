from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.

class Budget(models.Model):
    titre = models.TextField()
    date = models.DateField(default = now)
    owner = models.ForeignKey(to = User, on_delete = models.CASCADE)
    total = models.TextField()

    class Meta:
        ordering: ['-date']

class Depense(models.Model):
    
    ACTIF = 'ACTIF'
    ACHEVE = 'ACHEVE'
    STATUS_CHOICES = [
        (ACTIF, 'Freshman'),
        (ACHEVE, 'Sophomore'),
    ]
    
    designation = models.TextField()
    prix_unitaire = models.TextField()
    quantite = models.IntegerField()
    description = models.TextField()
    owner = models.ForeignKey(to = User, on_delete = models.CASCADE)
    budget = models.ForeignKey(to = Budget, on_delete = models.CASCADE)
    total = models.TextField()
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default=ACTIF,)

    def __str__(self):
        return self.designation
