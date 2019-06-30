from django.shortcuts import render, redirect
from django.http import HttpResponse
import os.path
import base64

from utils.Ciphers import AESCipher as aes
def index(request):
	return render(request, 'encryptedFiles/index.html')

def uploadFiles(request):
	if request.method == 'POST':
		key = request.POST['clave']
		file = request.FILES['archivos'].read().decode('utf-8')
		varaux = request.FILES['archivos'].name
		varaux = varaux.replace(" ", "_")
		filename = (varaux + ".enc") 
		content = encrypt(key,file)
		response = HttpResponse(content)
		response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
		return response

	else:
		return redirect('files:index')

def decryptFile(request):
	if request.method == 'POST':
		key = request.POST['clave']
		file = request.FILES['archivos'].read().decode('utf-8')
		varaux = request.FILES['archivos'].name
		splittedlist = varaux.split(".")
		extension = splittedlist[1]
		filename = ".".join(splittedlist[:-1])
		content = decrypt(key, file)
		response = HttpResponse(content.decode('utf-8'),content_type=None)
		response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
		return response
	else:
		return redirect('files:index')

def encrypt(key,text):
	key = str(key)
	cipher = aes(key)
	return cipher.encrypt(str(text))

def decrypt(key,text):
	key = str(key)
	cipher = aes(key)
	return cipher.decrypt(str(text))