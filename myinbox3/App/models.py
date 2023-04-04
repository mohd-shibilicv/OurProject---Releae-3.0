from django.db import models
from django.utils.html import format_html
from django.contrib.auth.models import User


class Customer(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Read', 'Read'),
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    phone = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    subject = models.CharField(max_length=30)
    message = models.TextField(max_length=1000)
    file = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=STATUS)

    # Control read and unread message on admin.py
    def situation(self):
        if self.status == 'Read':
            return format_html('<span style="color:black">{0}</span>', self.status)
        else:
            return format_html('<span style="color:red">{0}</span>', self.status)
    situation.allow_tags = True

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "inbox"


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    user_input = models.TextField( verbose_name="User Input", null=True)
    ai_response = models.TextField( verbose_name="User Input", null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'