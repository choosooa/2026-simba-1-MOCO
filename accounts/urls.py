from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('signup/', signup, name='signup'),
    path('signup/terms/', terms_detail, name='terms_detail'),
]