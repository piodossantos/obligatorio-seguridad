from django.urls import path, include

from encryptedFile.views import index, uploadFiles, decryptFile
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('',login_required( index), name='index'),
    path('uploadFiles',login_required(uploadFiles),name='uploadFiles'),
    path('decryptFile',login_required(decryptFile), name='decryptFile')

]
