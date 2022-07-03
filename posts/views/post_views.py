from django.shortcuts import render, redirect, get_object_or_404
from ..models import Post, Pattern, CommentForPost 
from ..forms import PostForm, PatternForm, CommentForPostForm
import json
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q

# Create your views here.
def main_index(request):
    recent_posts = Post.objects.order_by('-created_at')[:5]
    most_liked_posts = Post.objects.order_by('-likes')[:5]
    recent_patterns = Pattern.objects.order_by('-created_at')[:3]
    context = {'recent_posts': recent_posts,'most_liked_posts':most_liked_posts, 'recent_patterns':recent_patterns}
    return render(request, 'posts/main_index.html', context)

def posts_index(request):
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')  # 검색어
    posts = Post.objects.order_by('-created_at')
    if kw:
        posts = posts.filter(
            Q(title__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            #Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw)   # 질문 글쓴이 검색
            #Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
    paginator = Paginator(posts, 10)# 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'posts': page_obj, 'page': page, 'kw': kw}
    return render(request, 'posts/posts_index.html', context)


@login_required(login_url='common:login')
def posts_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.save()
            return redirect('posts:posts_index')
    else:
        form = PostForm()

    return render(request, 'posts/posts_create.html', {'form': form})


def posts_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = CommentForPost.objects.filter(post=post_id)

    if request.method == "POST":
        form = CommentForPostForm(request.POST)

        if form.is_valid():
            comment = form.save(commit = False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('posts:posts_detail', post_id)
    else:
        form = CommentForPostForm()

    context = {'post': post, 'comments': comments, 'form': form}
    return render(request, 'posts/posts_detail.html', context)

def post_like(request, post_id):
    like_b = get_object_or_404(Post, id=post_id)
    if request.user in like_b.liked_users.all():
        like_b.liked_users.remove(request.user)
        like_b.likes -= 1
        like_b.save()
    else:
        like_b.liked_users.add(request.user)
        like_b.likes += 1
        like_b.save()
    return redirect('posts:posts_detail', post_id)

@login_required(login_url='common:login')
def post_modify(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('posts:posts_detail', post_id=post.id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.modify_date = timezone.now()  # 수정일시 저장
            post.save()
            return redirect('posts:posts_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    context = {'form': form}
    return render(request, 'posts/posts_create.html', context)

@login_required(login_url='common:login')
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('posts:posts_detail', post_id=post.id)
    post.delete()
    return redirect('posts:posts_index')


