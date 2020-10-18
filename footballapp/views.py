from django.shortcuts import render
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from .models import TeamDetails, TeamMatches
from .serializers import FixtureSerializer, TeamListSerializer
from datetime import date, timedelta
from django.db.models import Q
import random
from rest_framework.pagination import PageNumberPagination
import math


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def loginadmin(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    # authenticating a user
    user = authenticate(username=username, password=password)
    if not user:  # unauthenticated user
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def getteamcount(request):
    team_count = TeamDetails.objects.all().count()
    # makefixture()
    return Response({'count': team_count},
                    status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def addteam(request):
    teamname = request.data.get("teamname")
    players = request.data.get("players")
    coach = request.data.get("coachname")
    manager = request.data.get("managername")
    if teamname is None or players is None or coach is None or manager is None:
        return Response({'error': 'All fields are required'},
                        status=HTTP_400_BAD_REQUEST)
    team_instance = TeamDetails(
        name=teamname,
        players=players,
        coach=coach,
        manager=manager
    )
    x = team_instance.save()
    team_count = TeamDetails.objects.all().count()
    if(team_count == 10):
        makefixture()
    return Response({'msg': 'success'},
                    status=HTTP_200_OK)


def makefixture():
    sdate = date(2023, 8, 1)   # start date
    edate = date(2023, 8, 23)   # end date

    delta = edate - sdate

    match_teams = list(TeamDetails.objects.all())  # [1,2,3,4,5,6,7,8,9,10]

    middle_index = int(len(match_teams)/2)

    temp_teams_list = []

    matches = []

    temp_teams_list.append(match_teams[:middle_index])  # [[1,2,3,4,5]]
    secondhalf = match_teams[middle_index:]  # [6,7,8,9,10]
    secondhalf.reverse()  # [10,9,8,7,6]
    temp_teams_list.append(secondhalf)  # [[1,2,3,4,5],[10,9,8,7,6]]

    for i in range(0, 9):
        left_jumper = temp_teams_list[1][0]
        right_jumper = temp_teams_list[0][4]

        temp_teams_list[0][4] = temp_teams_list[0][3]
        temp_teams_list[0][3] = temp_teams_list[0][2]
        temp_teams_list[0][2] = temp_teams_list[0][1]
        temp_teams_list[0][1] = left_jumper

        temp_teams_list[1][0] = temp_teams_list[1][1]
        temp_teams_list[1][1] = temp_teams_list[1][2]
        temp_teams_list[1][2] = temp_teams_list[1][3]
        temp_teams_list[1][3] = temp_teams_list[1][4]
        temp_teams_list[1][4] = right_jumper

        for j in range(0, 5):
            matches.append([temp_teams_list[0][j], temp_teams_list[1][j]])

    scheduled = []
    venue = ['Kerala', 'Punjab', 'Tamilnadu', 'Delhi', 'Banglore']

    match_objects = []
    for d in range(delta.days + 1):
        i = 0
        day = sdate + timedelta(days=d)
        for match in matches:
            scheduled.append([day, match, random.choice(venue)])
            match_instance = TeamMatches(
                date=day, team_a=match[0], team_b=match[1], venue=random.choice(venue))
            match_objects.append(match_instance)
            matches.remove(match)
            i = i + 1
            if(i == 2):
                break
    TeamMatches.objects.bulk_create(match_objects)


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'per_page': self.page.paginator.per_page,
                'last_page': math.ceil(self.page.paginator.count/self.page.paginator.per_page),
                'current': self.page.number

            },
            'count': self.page.paginator.count,
            'results': data
        })


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def matchfixturedata(request):
    match_fixture_data = TeamMatches.objects.all().order_by('id')
    paginator = CustomPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(match_fixture_data, request)
    match_fixture_data_serializer = FixtureSerializer(
        result_page, many=True)

    return paginator.get_paginated_response(match_fixture_data_serializer.data)


@csrf_exempt
@api_view(["POST"])
def updatePoints(request):
    team_a_point = request.data.get("teamapoint")
    team_b_point = request.data.get("teambpoint")
    match_id = request.data.get("matchId")

    match_instance = TeamMatches.objects.get(id=match_id)
    match_instance.team_a_points = team_a_point
    match_instance.team_b_points = team_b_point
    match_instance.save()
    return Response({'msg': 'success'},
                    status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
def getallteams(request):
    team_list_data = TeamDetails.objects.all()
    team_list_data_serializer = TeamListSerializer(team_list_data, many=True)
    return Response(team_list_data_serializer.data)


@csrf_exempt
@api_view(["GET"])
def teamDetails(request, team_id):
    team_details = TeamDetails.objects.get(id=team_id)
    team_details_serializer = TeamListSerializer(team_details, many=False)
    team_matches = None
    team_count = TeamDetails.objects.all().count()
    if(team_count == 10):
        team_matches_data = TeamMatches.objects.filter(
            Q(team_a=team_id) | Q(team_b=team_id))
        team_matches_data_serializer = FixtureSerializer(
            team_matches_data, many=True)
        team_matches = team_matches_data_serializer.data
    return Response({'fixtures': team_matches, 'team': team_details_serializer.data})
