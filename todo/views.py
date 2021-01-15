from django.shortcuts import render
from .models import Bucket, Todo
import json
from django.http import HttpResponse, FileResponse,JsonResponse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache

# Serve Single Page Application
home = never_cache(TemplateView.as_view(template_name='index.html'))
# Create your views here.
@csrf_exempt
def index(request,username):
    print("USERNAME : ",username)
    user = User.objects.get(username=username)
    print("USER ID : ---",user.id)
    if request.method == "POST":
        req = json.loads(request.body.decode('utf-8'))
        print(req)
        text = req['text']
        bucket = req['bucket']
        #check if the bucket element already exists
        
        if Bucket.objects.filter(name=bucket.capitalize(),user=user).exists():
             bucket_id = Bucket.objects.get(name=bucket.capitalize(),user=user).id
             todo_data = Todo(text=text,bucket_id=bucket_id,user=user)
             todo_data.save()
        else:
        #if a new bucket is being created
            bucket_data = Bucket(name=bucket.capitalize(),user=user)
            bucket_data.save()
            bucket_id = Bucket.objects.get(name=bucket.capitalize(),user=user).id
            todo_data = Todo(text=text,bucket_id=bucket_id,user=user)
            todo_data.save()

    todo_list = Todo.objects.filter(user=user).order_by('-created_at')
    json_todo = list(todo_list.values())
    return JsonResponse(json_todo,safe=False)

@csrf_exempt
def buckets(request,username):
    user = User.objects.get(username=username)
    buckets = Bucket.objects.filter(user=user)
    json_bucket = list(buckets.values()) 
    print("JSON BUKCEASDASDASDA : ",json_bucket)
    return JsonResponse(json_bucket,safe=False)

@csrf_exempt
def complete_task(request, username, id):
    user = User.objects.get(username=username)
    todo_item = Todo.objects.get(id=int(id),user=user)
    todo_item.status = not todo_item.status
    todo_item.completed_at = datetime.now()
    todo_item.save()
    json_todo_item = { key : value for key,value in todo_item.__dict__.items() if key!='_state' }
    print(json_todo_item)
    return JsonResponse(json_todo_item,safe=False)

@csrf_exempt
def delete_task(requests,id,username):
    user = User.objects.get(username=username)
    todoItem = Todo.objects.get(id = id,user=user)
    todoItem.delete()
    todo_list = Todo.objects.filter(user=user).order_by('-created_at')
    json_todo = list(todo_list.values())
    return JsonResponse(json_todo,safe=False)

@csrf_exempt
def todo_item_detail(request,id,username):
    user = User.objects.get(username=username)
    if request.method == "POST":
        
        req = json.loads(request.body.decode('utf-8'))
        print(req)
        text = req['text']
        bucket = req['bucket']
        todo_item = Todo.objects.get(id=id,user=user)
        todo_item.text = text
        if Bucket.objects.filter(name=bucket.capitalize(),user=user).exists():
             bucket_id = Bucket.objects.get(name=bucket.capitalize(),user=user).id
             todo_item.bucket_id = bucket_id
        else:
            bucket_data = Bucket(name=bucket.capitalize(),user=user)
            bucket_data.save()
            bucket_id = Bucket.objects.get(name=bucket.capitalize(),user=user).id
            todo_item.bucket_id = bucket_id
        todo_item.save()
        todo_list = Todo.objects.filter(user=user).order_by('-created_at')
        json_todo = list(todo_list.values())
        return JsonResponse(json_todo,safe=False)
    else:
        
        todo_item = Todo.objects.get(id = id,user=user)
        json_todo_item = { key : value for key,value in todo_item.__dict__.items() if key!='_state' }
        print(json_todo_item)
        return JsonResponse(json_todo_item,safe=False)

@csrf_exempt
def delete_bucket(request,bucket_id,username):
    user = User.objects.get(username=username)
    bucket_to_delete = Bucket.objects.get(id=bucket_id,user=user)
    bucket_to_delete.delete()
    buckets = Bucket.objects.filter(user=user)
    json_bucket = list(buckets.values())
    print(json_bucket)
    return JsonResponse(json_bucket,safe=False)