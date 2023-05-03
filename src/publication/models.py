from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy

User = get_user_model()


class PostType(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'type de publication'


class Filter(models.Model):
    name = models.CharField(max_length=128, unique=True)
    details = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'filtre'


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='utilisateur')
    type = models.ForeignKey(PostType, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    creation_date = models.DateTimeField(gettext_lazy("creation date"), default=timezone.now)

    def __str__(self):
        return f"{self.user.username} ({self.type}) - {self.creation_date}"

    class Meta:
        verbose_name = 'Post'


class PostMedia(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    filter = models.ForeignKey(Filter, blank=True, null=True, on_delete=models.SET_NULL)
    thumbnail = models.ImageField(upload_to='posts')


class Effect(models.Model):
    post_media = models.ManyToManyField(PostMedia)
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'effet'


class Comment(models.Model):
    # replied = models.ForeignKey(Comment, blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='utilisateur')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    creation_date = models.DateTimeField(gettext_lazy("creation date"), default=timezone.now)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'commentaire'


class Reaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='utilisateur')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

