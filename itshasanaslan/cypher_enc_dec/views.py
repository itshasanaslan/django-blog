from types import resolve_bases
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .crypto import CryptoHandler
# Create your views here.
from django.views.decorators.csrf import csrf_exempt



@api_view(["GET","POST"])
def main_page(request):
    if request.method == "GET":
        return render(request, 'cypher_base.html')
    else:
        text = request.POST.get("text_area_value")
        if text == None : return None

        return {"data":"Hello world1."}


@api_view(["POST", "GET"])
def generate_key(requests):
    crypto_handler = CryptoHandler(save = False, generate_new = True)
    data = {
        "cypherKey" : crypto_handler.key.decode()
    }

    if requests.method == "GET":
       return HttpResponse(str(data))
    if requests.method == "POST":
       return Response(data)


@api_view(["POST", "GET"])
def encrypt(requests):
    if requests.method == "POST":
        key = requests.data.get("key")
        if not key:
            return Response({"Message": "Key not found"})
        c = CryptoHandler(key = key)
        msg = requests.data.get("text")
        if not msg:
            return Response({"Message": "Text not found"})
        encryted = c.encrypt(msg)
        return Response({"encryptedText": encryted})
    else:
        return HttpResponse("Hello")

@api_view(["POST", "GET"])
def decrypt(requests):
    key = requests.data.get("key")
    if not key:
        return Response({"Message": "Key not found"})
    c = CryptoHandler(key = key)
    msg = requests.data.get("text")
    if not msg:
        return Response({"Message": "Text not found"})
    decryted = c.decrypt(msg.encode())
    return Response({"decryptedText": decryted})

@api_view(["POST", "GET"])
def source_code(requests):
    p = "/var/www/itshasanaslan/cypher_enc_dec/crypto.py"
    with open(p, 'r') as file:
        data = file.read()
    return HttpResponse(data, content_type="text/plain")


