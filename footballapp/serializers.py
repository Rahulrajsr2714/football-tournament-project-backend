from rest_framework import serializers
from .models import TeamDetails, TeamMatches


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamDetails
        fields = ["name"]


class FixtureSerializer(serializers.ModelSerializer):
    team_a = TeamSerializer(read_only=True)
    team_b = TeamSerializer(read_only=True)

    class Meta:
        model = TeamMatches
        fields = ('__all__')


class TeamListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamDetails
        fields = ('__all__')
