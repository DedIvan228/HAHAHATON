from django.contrib.auth.models import AbstractUser
from django.db import models
import os

def avatar_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f"avatar_{instance.id}{ext}"
    return os.path.join("avatar", filename)

class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'Обычный'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

class Room(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms')
    created_at = models.DateTimeField(auto_now_add=True)

class Team(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='teams')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_teams')
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User, related_name='teams')

class Rool(models.Model):
    ROLE_CHOICES = [
        ('user', 'Обычный'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    ]
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='rools')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='rools', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rools')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'К выполнению'),
        ('in_progress', 'В процессе'),
        ('done', 'Выполнено'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    deadline = models.DateTimeField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tasks')
    tags = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='tasks', null=True)