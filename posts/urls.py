from django.contrib import admin
from django.urls import path, include
from .views import post_views, pattern_views

app_name = 'posts'
urlpatterns = [
    path('posts_index/', post_views.posts_index, name='posts_index'),
    path('posts_create/', post_views.posts_create, name='posts_create'),
    path('posts_detail/<int:post_id>/', post_views.posts_detail, name='posts_detail'),
    path('post_like/<int:post_id>/', post_views.post_like, name="post_like"),
    path('post_modify/<int:post_id>/', post_views.post_modify, name='post_modify'),
    path('post_delete/<int:post_id>/', post_views.post_delete, name='post_delete'),
    
    path('patterns_index/', pattern_views.patterns_index, name='patterns_index'),
    path('patterns_create/', pattern_views.patterns_create, name='patterns_create'),
    path('patterns_detail/<int:pattern_id>/', pattern_views.patterns_detail, name='patterns_detail'),
    path('pattern_like/<int:pattern_id>/', pattern_views.pattern_like, name="pattern_like"),
    path('pattern_modify/<int:pattern_id>/', pattern_views.pattern_modify, name='pattern_modify'),
    path('pattern_delete/<int:pattern_id>/', pattern_views.pattern_delete, name='pattern_delete'),

    path('', post_views.main_index, name='main_index'), #경로 추후에 수정

]
