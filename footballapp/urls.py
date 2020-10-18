from django.urls import path
from . import views


urlpatterns = [
    path('admin-login', views.loginadmin, name='adminlogin'),
    path('get-team-count', views.getteamcount, name='getteamcount'),
    path('add-team', views.addteam, name='addteam'),
    path('get-fixture', views.matchfixturedata, name='getfixture'),
    path('admin/update-point', views.updatePoints, name='updatepoints'),
    path('admin/get-all-teams', views.getallteams, name='getallteams'),
    path('admin/team-details/<int:team_id>',
         views.teamDetails, name='teamdetails'),

]
