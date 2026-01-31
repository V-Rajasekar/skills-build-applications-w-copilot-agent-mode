from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection
from djongo import models as djongo_models

from octofit_tracker import models as app_models

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        User = get_user_model()
        # Delete all data
        User.objects.all().delete()
        app_models.Team.objects.all().delete()
        app_models.Activity.objects.all().delete()
        app_models.Leaderboard.objects.all().delete()
        app_models.Workout.objects.all().delete()

        # Create Teams
        marvel = app_models.Team.objects.create(name='Team Marvel')
        dc = app_models.Team.objects.create(name='Team DC')

        # Create Users (Superheroes)
        ironman = User.objects.create_user(username='ironman', email='ironman@marvel.com', password='password', team=marvel)
        captain = User.objects.create_user(username='captainamerica', email='cap@marvel.com', password='password', team=marvel)
        batman = User.objects.create_user(username='batman', email='batman@dc.com', password='password', team=dc)
        superman = User.objects.create_user(username='superman', email='superman@dc.com', password='password', team=dc)

        # Create Activities
        app_models.Activity.objects.create(user=ironman, type='run', duration=30, distance=5)
        app_models.Activity.objects.create(user=captain, type='cycle', duration=45, distance=20)
        app_models.Activity.objects.create(user=batman, type='swim', duration=25, distance=1)
        app_models.Activity.objects.create(user=superman, type='run', duration=60, distance=10)

        # Create Workouts
        app_models.Workout.objects.create(name='Morning Cardio', description='Cardio for all heroes', suggested_for=marvel)
        app_models.Workout.objects.create(name='Strength Training', description='Strength for DC', suggested_for=dc)

        # Create Leaderboard
        app_models.Leaderboard.objects.create(team=marvel, points=100)
        app_models.Leaderboard.objects.create(team=dc, points=120)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
