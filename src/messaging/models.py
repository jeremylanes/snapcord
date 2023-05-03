from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Group(models.Model):
    name = models.CharField(max_length=128)
    slogan = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(User)
    creation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    # recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    # parent_message = models.ForeignKey(Message, null=True, blank=True, on_delete=models.SET_NULL)
    content = models.TextField()
    creation_date = models.DateTimeField(default=timezone.now)
    last_update_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.sender.username


class Recipient(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, blank=True, null=True, on_delete=models.CASCADE)
    message_recipient = models.ForeignKey(Message, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username if self.user else self.group.name
