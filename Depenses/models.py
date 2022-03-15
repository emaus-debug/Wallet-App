from unicodedata import category, name
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.

class Expenses(models.Model):
    amount = models.TextField()
    date = models.DateField(default = now)
    description = models.TextField()
    owner = models.ForeignKey(to = User, on_delete = models.CASCADE)
    category = models.CharField(max_length = 266)

    def __str__(self):
        return self.category


    class Meta:
        ordering: ['-date']
        verbose_name_plural = "Dépenses"

class Category(models.Model):
    name = models.CharField(max_length = 255)

    class Meta:
        verbose_name_plural = "Catégories"

    def __str__(self):
        return self.name
    
    