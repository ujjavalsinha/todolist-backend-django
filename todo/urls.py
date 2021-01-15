from django.contrib import admin
from django.urls import path, include
from .views import index,complete_task,buckets,delete_task,todo_item_detail,delete_bucket,home

urlpatterns = [
    path('', home, name='index'),
    path('todolist/<str:username>', index),
    path('todolist/<str:username>/<int:id>/complete',complete_task),
    path('buckets/<str:username>',buckets),
    path('todolist/<str:username>/<int:id>/delete',delete_task),
    path('todolist/<str:username>/<int:id>',todo_item_detail),
    path('buckets/<str:username>/<int:bucket_id>/delete',delete_bucket)
]