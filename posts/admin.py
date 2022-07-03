from django.contrib import admin

# Register your models here.
from .models import Post, Pattern, CommentForPost

admin.site.register(Post)
admin.site.register(Pattern)
admin.site.register(CommentForPost)