from Crypto.Hash import SHA256
from django.shortcuts import render, redirect
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import  PKCS1_v1_5

from io import BytesIO
from zipfile import ZipFile
from django.http import HttpResponse
import binascii

from utils.Ciphers import SHA256Cipher


def index(request):
	return render(request, 'signature/index.html')

def indexDigitalKey(request):
	return render(request, 'signature/digitalKey.html')

def generateKey(request):
	random_generator = Crypto.Random.new().read
	key=RSA.generate(1024,random_generator)
	publicKey,privateKey = key,key.publickey()

	in_memory = BytesIO()
	zip = ZipFile(in_memory,"a")
	zip.writestr("public.enc",publicKey.exportKey())
	zip.writestr("private.enc",publicKey.exportKey())
	for f in zip.filelist:
		f.create_system = 0

	zip.close()

	response = HttpResponse(zip,content_type="application/zip")
	response["Content-Disposition"] = "attachment; filename=keys.zip"

	in_memory.seek(0)
	response.write(in_memory.read())

	return response

def signDocument(request):
	file = request.FILES['documento'].read()
	privateKey = request.FILES['clave'].read()
	privateKey = RSA.importKey(privateKey)
	signer = PKCS1_v1_5.new(privateKey)
	sha = SHA256.new()
	sha.update(file)
	signature = signer.sign(sha)
	response = HttpResponse(signature, content_type='text/plain;')
	response['Content-Disposition'] = 'attachment; filename={0}'.format('sign.enc')
	return response


def validateSignature(request):
	signature = request.FILES['firma'].read()
	document = request.FILES['documento'].read()
	publicKey =request.FILES['clave'].read()
	publicKey = RSA.importKey(publicKey)

	signer = PKCS1_v1_5.new(publicKey)

	sha = SHA256.new()
	sha.update(document)  # Recurso

	result = signer.verify(sha, signature)
	if(result):
		return render(request, 'signature/index.html',{'verify_success':True})
	return render(request, 'signature/index.html',{'verify_failure':True})
