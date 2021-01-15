from django.shortcuts import render
from django.contrib.auth.models import User
import json
from django.http import HttpResponse, FileResponse,JsonResponse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login 
# Create your views here.
token = 'd94a4968565a11ebae930242ac130002'

@csrf_exempt
def signup(request):
    req = json.loads(request.body.decode('utf-8'))
    username = req['username']
    email = req['email']
    password = req['password']
    if User.objects.filter(username=username).exists():
        return JsonResponse({'message' : 'Username already exists'},status = 409)
    if User.objects.filter(email=email).exists():
        return JsonResponse({'message' : 'Email already exists'},status = 409)
    user_data,created = User.objects.get_or_create(username=username,email=email)
    user_data.set_password(password)
    user_data.save()
    return JsonResponse({'tokenId':token, 'username':username},safe=False)

@csrf_exempt
def login(request):
    req = json.loads(request.body.decode('utf-8'))
    username = req['username']
    password = req['password']
    user = authenticate(request, username=username,password=password)
    if user is not None:
        return JsonResponse({'tokenId' : token,'username' : username})
    else:
        return JsonResponse({'message' : "Invalid credentials"},status = 401)