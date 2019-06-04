from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .models import data
import requests
import zipcodetw
import pyqrcode

def index(request):
    return render(request, 'index.html', {})

def post_form(request):
    receiverAddressID = str(zipcodetw.find(request.GET['receiverAddress']))
    print(receiverAddressID)
    data_instance = data.objects.create(receiverName = request.GET['receiverName'],
        senderName = request.GET['senderName'],
        receiverAddress = request.GET['receiverAddress'],
        receiverAddressID = receiverAddressID,
        senderAddress = request.GET['senderAddress'],
        phone = request.GET['phone'],
        kind = request.GET['kind'], 
        amount = request.GET['amount'])
    return JsonResponse({'id': data_instance.id, 'url': '/success/' + str(data_instance.id)})

def getInfo(request, id):
    info = data.objects.filter(id=id).first()
    return JsonResponse(model_to_dict(info))

def qrcode(request, id):
    info = data.objects.filter(id=id).first()
    id = str(info.id)
    img=pyqrcode.create(id)
    img.png('statics/url.png', scale=8)
    return render(request, 'success.html', {})