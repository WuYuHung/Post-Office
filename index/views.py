from django.shortcuts import render
from django.http import JsonResponse
from .models import data

def index(request):
    return render(request, 'index.html', {})

def post_form(request):
    data_instance = data.objects.create(receiverName = request.GET['receiverName'],
        senderName = request.GET['senderName'],
        receiverAddress = request.GET['receiverAddress'],
        senderAddress = request.GET['senderAddress'],
        phone = request.GET['phone'],
        kind = request.GET['kind'], 
        amount = request.GET['amount'])
    return JsonResponse({})