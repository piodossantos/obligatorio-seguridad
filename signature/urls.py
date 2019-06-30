from django.urls import path, include

from signature.views import *

urlpatterns = [
    path('', index, name='index'),
    path('keys',generateKey,name="generateKey"),
    path('sign', signDocument, name="sign"),
    path('verify', validateSignature, name="verify")
]
