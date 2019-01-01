from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Team(models.Model):
    """
    Une équipe scrum est un ensemble de personnes qui travaillent sur un projet
    """
    member = models.ManyToManyField(User)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Equipe"
        verbose_name_plural = "Equipes"


class Project(models.Model):
    """
    La representation d'un projet dans le system
    Un projet est prise en charge par une équipe
    """
    team = models.ForeignKey(Team)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"


class ProductBacklog(models.Model):
    """
    Un backlog produit Scrum contient un ensemble de user storie
    Chaque backlog est systèmatiquement rattaché à un projet.
    """
    team = models.ForeignKey(Team)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Backlog de Produit"
        verbose_name_plural = "Backlog des produits"

class Sprint(models.Model):
    """
    Un Sprint est une idtération réalisée par une équipe
    Dans un sprint, une équipe peut travailler sur plusieurs projets.
    """
    team = models.ForeignKey(Team)
    begin_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Itération"
        verbose_name_plural = "Itérations"


class UserStory(models.Model):
    """
    Une user story est une demande client
    """
    product_backlog = models.ForeignKey(ProductBacklog)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Demande client"
        verbose_name_plural = "Demandes client"