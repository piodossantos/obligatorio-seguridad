from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from utils import Ciphers
from django.contrib.auth import authenticate, login
from django.db import connection
ERROR_MESSAGE = "Error de autenticacion, Usuario y/o contraseña incorrectas."

def index(request,error_message=None):
    context = {}
    if error_message!= None:
        context = {'error_message':error_message}
    return render(request, 'authentication/index.html',context)

def verifyCredentials(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        validateUsername= str(username).replace(".","")
        if(not str(validateUsername).isalnum()):
            return index(request,"El nombre de usuario debe contener solamente caracteres alfanumericos")

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM auth_user WHERE username='"+ username +"' LIMIT 1;")
        json = cursor.fetchone()
        if json==None:
            return index(request,ERROR_MESSAGE)
        hashedPassword  = Ciphers.SHA256Cipher().hash(text=password)
        passwordBackend = json[1].split("$")[-1]
        if passwordBackend == None:
            return index(request,ERROR_MESSAGE)
        if passwordBackend == hashedPassword:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
    return index(request, ERROR_MESSAGE)



