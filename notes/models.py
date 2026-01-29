from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    likes = models.ManyToManyField(User, related_name='liked_notes', blank=True)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()
