from django.db import models
from . import views
from django.contrib.auth.models import User

# Create your models here.

class chatlog(models.Model):

    chatuserid = models.ForeignKey(User, on_delete=models.CASCADE)
    textmessage = models.TextField()
    timestamp=models.DateTimeField(auto_now_add= True)
    