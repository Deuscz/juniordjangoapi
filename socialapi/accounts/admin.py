from django.contrib import admin
from accounts.models import Account
from posts.models import Post
# Register your models here.
admin.site.register(Account)
admin.site.register(Post)