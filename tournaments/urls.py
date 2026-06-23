from django.urls import path
from .views import *

app_name = "tournaments"

urlpatterns = [
    path("", tournament_main, name="main"),
    path("create/", tournament_create, name="create"),
    path("<int:pk>/play/", tournament_play, name="play"),
    path("<int:pk>/result/", tournament_result, name="result"),
    path("<int:pk>/share/", tournament_link, name="create_share"),
    path("<int:pk>/restart/", tournament_restart, name="restart"),
    path("share/<uuid:token>/", shared_intro, name="shared_intro"),
    path("share/<uuid:token>/play/", shared_play, name="shared_play"),
    path("<int:pk>/link/", tournament_link, name="link"),
    path("record/", tournament_record, name="record"),  ## url 연결 'tournaments:record'로 하시면 됩니다
]