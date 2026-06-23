from django.urls import path
from .views import *

app_name = 'items'

urlpatterns = [
    path('storage/', storage, name='storage'),
    path('search/', search, name='search'),
    path('create/', create, name='create'),
    path('detail/<int:item_id>/', detail, name='detail'),
    path('edit/<int:item_id>/', edit, name='edit'),
    path('scrap/<int:item_id>/', scrap, name='scrap'),
    path('scrapped_list/', scrapped_list, name='scrapped_list'),
    path('delete/<int:item_id>/', delete, name='delete'),
    path('main/', main, name='main'),
    path('plus_info/', plus_info, name='plus_info'),
    path('plus/', plus, name='plus'),
    path('detail/<int:item_id>/', detail, name='detail'),
]