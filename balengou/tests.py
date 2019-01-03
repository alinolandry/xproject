from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from .models import *
# Create your tests here.

class BalengouTest(TestCase):

    def setUp(self):
        # Initialisation des données de test
        self.pascal = User.objects.create_user('pascal', 'pascal@balengou.com', 'pascal@balengou.com')
        self.john = User.objects.create_user('john', 'john@balengou.com', 'john@balengou.com')
        self.jimi = User.objects.create_user('jimi', 'jimi@balengou.com', 'jimi@balengou.com')
        self.gaston = User.objects.create_user('gaston', 'gaston@balengou.com', 'gaston@balengou.com')

        self.fo_team = Team.objects.create(name='Front Office Team')
        self.fo_team.members.add(self.pascal)
        self.fo_team.members.add(self.john)

        self.bo_team = Team.objects.create(name='Back Office Team')
        self.bo_team.members.add(self.jimi)
        self.bo_team.members.add(self.gaston)

        self.fo_backlog = ProductBacklog.objects.create(team=self.fo_team, name="Backlog de l'équipe de front")
        self.bo_backlog = ProductBacklog.objects.create(team=self.bo_team, name="Backlog de l'équipe de back")

        self.fo_backlog_story_1 = UserStory.objects.create(product_backlog=self.fo_backlog, name="Nouvelle présentation de la fiche article")
        self.fo_backlog_story_2 = UserStory.objects.create(product_backlog=self.fo_backlog, name="Insertion auto de keyword dans les balises alt")

        self.bo_backlog_story_1 = UserStory.objects.create(product_backlog=self.bo_backlog, name="Ajout de l'autocompletion pour la recherche de produits")
        self.bo_backlog_story_2 = UserStory.objects.create(product_backlog=self.bo_backlog, name="Correction des fautes de de grammaire sur le site")

    def test_dashboard_not_authenticated_user(self):
        # Test case qui nous rassure que l'utilisateur ne sera pas à dasboard s'il n'est as authentifié
        url = reverse("balengou:dashboard")
        self.client = Client()
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, "balengou/dashboard.html")
        self.failUnlessEqual(response.status_code, 302)

    def test_dashboard_authenticated_user(self):
        self.client = Client()
        # Test de l'afficharge du dasboard quand l'utilisateur est bien connecté
        self.client.login(username="pascal", password="pascal@balengou.com")
        response = self.client.get(reverse('balengou:dashboard'))
        self.assertEqual(type(response.context['backlogs']), QuerySet)
        self.assertEqual(len(response.context['backlogs']), 2)
        self.assertEqual(type(response.context['teams']), QuerySet)
        self.assertEqual(len(response.context['teams'], 2))
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'balengou:dashboard.html')
        self.client.logout() 

    def test_backlog_not_authenticated_user(self):
        self.client = Client()
        response = self.client.get(reverse('balengou:backlog', kwargs={'backlog_id':1}))
        self.assertTemplateNotUsed(response, 'balengou/backlog.html')
        self.failUnlessEqual(response.status_code, 302)
    
    def test_backlog_authentificated_user(self):
        self.client = Client()
        self.client.login(username="pascal", password="pascal@balengou.com")
        response = self.client.get(reverse('balengou:backlog', kwargs={'backlog_id':1})) # L'id 1 correspond au backlog de fo_backlog
        self.assertEqual(response.context['backlog'], self.fo_backlog)
        self.assertEqual(type(response.context['stories']), QuerySet)
        self.assertEqual(len(response.context['stories']), 2)
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "balengou:backlog.html")
        self.client.logout()