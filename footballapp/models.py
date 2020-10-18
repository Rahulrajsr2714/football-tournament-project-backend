from django.db import models

# Create your models here.


class TeamDetails(models.Model):
    name = models.CharField(max_length=100, unique=True)
    players = models.CharField(max_length=1000)
    coach = models.CharField(max_length=100)
    manager = models.CharField(max_length=100)


class TeamMatches(models.Model):
    team_a = models.ForeignKey(
        TeamDetails, on_delete=models.CASCADE, null=False, blank=False, related_name='teama')
    team_b = models.ForeignKey(
        TeamDetails, on_delete=models.CASCADE, null=False, blank=False, related_name='teamb')
    venue = models.CharField(max_length=100)
    date = models.DateTimeField()
    team_a_points = models.IntegerField(null=True)
    team_b_points = models.IntegerField(null=True)
