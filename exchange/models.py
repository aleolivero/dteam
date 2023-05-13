from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    readers = models.ManyToManyField(User, related_name='read_chats', blank=True)






