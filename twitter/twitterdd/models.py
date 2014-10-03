from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Tweet(models.Model):
	username = models.ForeignKey(User)
	text = models.CharField(max_length=140)
	timestamp = models.DateTimeField(auto_now_add=True)

class Followers(models.Model):
	username1 = models.ForeignKey(User, related_name='followee')
	username2 = models.ForeignKey(User, related_name='follower')
