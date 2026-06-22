from django.urls import path
from . import views

urlpatterns = [
    path('', views.plus_info, name='plus_info'),
    path('plus/', views.plus, name='plus'),
    path('product/', views.product, name='product'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('agree/', views.agree, name='agree'),
    path('main/', views.main, name='main'),
    path('start/', views.cup_start, name='cup_start'),
    path('select/', views.cup_select, name='cup_select'),
    path('ing/', views.cup_ing, name='cup_ing'),
    path('result/', views.cup_result, name='cup_result'),
    path('link/', views.cup_link, name='cup_link'),
    path('share/preview/', views.cup_share_preview, name='cup_share_preview'),
    path('result/preview/', views.cup_result_preview, name='cup_result_preview'),
    path('share/<str:share_token>/', views.cup_share, name='cup_share'),
    path('share/<str:share_token>/start/', views.cup_share_start, name='cup_share_start'),
]
