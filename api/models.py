from django.db import models
from datetime import datetime   
from django.conf import settings    


# Create your models here.
class Note(models.Model):
    title=models.CharField(max_length=100)
    text=models.CharField(null=True,blank=True,max_length=1000)
    date = models.DateTimeField(auto_now=True,null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
