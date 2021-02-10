from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Create your models here.
class CustomUser(AbstractUser):
    dob = models.DateField()

class Feeds(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateTimeField()

class Like(models.Model):
    user1 =  models.ForeignKey(CustomUser, on_delete=models.CASCADE)  
    feeds1 = models.ForeignKey(Feeds, on_delete=models.CASCADE)

class Dislike(models.Model):
    user1 =  models.ForeignKey(CustomUser, on_delete=models.CASCADE)  
    feeds1 = models.ForeignKey(Feeds, on_delete=models.CASCADE) 

class Comments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateTimeField()
 