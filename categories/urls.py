from django.urls import path
from .views import *

app_name = 'categories'

urlpatterns = [
    path('create/', create, name='create'),
    path('<int:category_id>/delete/', delete, name='delete'),
    path('<int:category_id>/edit/', edit, name='edit'),
    path('current/', current, name='current'),
]