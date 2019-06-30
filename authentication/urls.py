from django.urls import path

from authentication.views import index,verifyCredentials
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import logout_then_login

urlpatterns = [
    path('', login_required(index), name='index'),
    path('login',verifyCredentials,name="login"),
    path('logout', logout_then_login, name='logout'),

]
