from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Todo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    text = models.TextField(max_length=300)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    bucket = models.ForeignKey('Bucket', on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class Bucket(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length = 50)

    def __str__(self):
        return self.name