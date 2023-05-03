from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone

from SnapCord.settings import EMAIL_HOST_USER

User = get_user_model()
snapcord_mail_address = EMAIL_HOST_USER


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='expéditeur')
    readed = models.BooleanField(default=False, verbose_name='lu')
    name = models.CharField(max_length=128, default='inconu', verbose_name="nom de l'éxpediteur")
    email = models.EmailField(verbose_name='adresse mail')
    subject = models.CharField(max_length=1024, blank=True, verbose_name='sujet')
    content = models.TextField(max_length=128000, verbose_name='contenu du message')
    sending_date = models.DateTimeField(default=timezone.now, verbose_name="date d'envoi")

    class Meta:
        verbose_name = 'Message'

    def __str__(self):
        return self.name


class BroadcastEmail(models.Model):
    broadcast = models.BooleanField(default=False, verbose_name='message difusé')
    subject = models.CharField(max_length=1024, verbose_name='sujet')
    message = models.TextField(max_length=128000, verbose_name='contenu du mail ')
    sending_date = models.DateTimeField(default=timezone.now, verbose_name="date d'envoi")

    class Meta:
        verbose_name = 'Diffusion de mail'

    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs):
        if self.broadcast:
            global snapcord_mail_address
            users = User.objects.filter(is_staff=False)
            users_mails_address = [x.email for x in users]

            send_mail(
                subject=self.subject,
                message=self.message,
                from_email=snapcord_mail_address,
                recipient_list=users_mails_address,
                fail_silently=False
            )
        return super().save(*args, **kwargs)
