from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    title = models.CharField('',max_length=20)
    content = models.TextField('',max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    author= models.ForeignKey(User, on_delete=models.CASCADE)
    liked_users = models.ManyToManyField(User, related_name='post_likes',blank=True)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class CommentForPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField('',max_length=500)
    created_at = models.DateField(auto_now_add=True)
    author= models.ForeignKey(User, on_delete=models.CASCADE)


class Pattern(models.Model):
    title= models.CharField('',max_length=20)
    author= models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    liked_users = models.ManyToManyField(User, related_name='pattern_likes',blank=True)
    likes = models.PositiveIntegerField(default=0)
    color_list = models.JSONField()
    pattern_list = models.JSONField()
    row_length = models.IntegerField(default=0)
    col_length = models.IntegerField(default=0)
    comment= models.TextField('',max_length=500)