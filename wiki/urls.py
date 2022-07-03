from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'wiki'

urlpatterns = [
    path('wiki_post_index/', views.wiki_post_index, name='wiki_post_index'),
    path('wiki_post_create/', views.wiki_post_create, name='wiki_post_create'),
    path('wiki_post_detail/<str:wiki_post_name>/', views.wiki_post_detail, name='wiki_post_detail'),
    path('wiki_post_modify/<str:wiki_post_name>/', views.wiki_post_modify, name='wiki_post_modify'),
    # path('wiki_post_delete/<str:wiki_post_name>/', views.wiki_post_delete, name='wiki_post_delete'),
    path('wiki_post_history/<str:wiki_post_name>/', views.wiki_post_history, name='wiki_post_history'),
    path('wiki_post_history_revert/<str:wiki_post_name>/<int:wiki_history_id>/', views.wiki_post_history_revert, name='wiki_post_history_revert'),
    path('wiki_post_history_detail/<str:wiki_post_name>/<int:wiki_history_id>/', views.wiki_post_history_detail, name='wiki_post_history_detail'),
]