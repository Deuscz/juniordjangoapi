from django.db import models
from django.db.models.signals import pre_save
from accounts.models import Account
from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False, unique=True)
    text = models.TextField(max_length=10000, blank=False, null=False)
    slug = models.SlugField(blank=True, unique=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    publish_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Account, blank=True, related_name='likes')

    def __str__(self):
        return self.slug

def pre_save_post(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


pre_save.connect(pre_save_post, sender=Post)
