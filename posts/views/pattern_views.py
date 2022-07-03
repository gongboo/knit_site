from django.shortcuts import render, redirect, get_object_or_404
from ..models import Post, Pattern, CommentForPost 
from ..forms import PostForm, PatternForm, CommentForPostForm
import json
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q


def patterns_index(request):
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')  # 검색어
    patterns = Pattern.objects.order_by('-created_at')
    if kw:
        patterns = patterns.filter(
            Q(title__icontains=kw) |  # 제목 검색
            #Q(content__icontains=kw) |  # 내용 검색
            #Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw)   # 질문 글쓴이 검색
            #Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
    paginator = Paginator(patterns, 9)# 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'patterns': page_obj}
    return render(request, 'posts/patterns_index.html', context)

@login_required(login_url='common:login')
def patterns_create(request):
    if request.method == "POST":
        form = PatternForm(request.POST)
        if form.is_valid():
            pattern = form.save(commit = False)
            pattern.author = request.user
            pattern.save()
            return redirect('posts:patterns_index')
    else:
        form = PatternForm()
    return render(request, 'posts/patterns_create.html', {'form': form})

def patterns_detail(request, pattern_id):
    pattern = Pattern.objects.get(id=pattern_id)
    context = {'pattern': pattern}
    return render(request, 'posts/patterns_detail.html', context)

def pattern_like(request, pattern_id):
    like_b = get_object_or_404(Pattern, id=pattern_id)
    if request.user in like_b.liked_users.all():
        like_b.liked_users.remove(request.user)
        like_b.likes -= 1
        like_b.save()
    else:
        like_b.liked_users.add(request.user)
        like_b.likes += 1
        like_b.save()
    return redirect('posts:patterns_detail', pattern_id)


@login_required(login_url='common:login')
def pattern_modify(request, pattern_id):
    pattern = get_object_or_404(Pattern, pk=pattern_id)
    if request.user != pattern.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('posts:patterns_detail', pattern_id=pattern.id)
    if request.method == "POST":
        form = PatternForm(request.POST, instance=pattern)
        if form.is_valid():
            pattern = form.save(commit=False)
            pattern.modify_date = timezone.now()  # 수정일시 저장
            pattern.save()
            return redirect('posts:patterns_detail', pattern_id=pattern.id)
    else:
        form = PatternForm(instance=pattern)
    context = {'form': form}
    return render(request, 'posts/patterns_create.html', context)

@login_required(login_url='common:login')
def pattern_delete(request, pattern_id):
    pattern = get_object_or_404(Pattern, pk=pattern_id)
    if request.user != pattern.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('posts:patterns_detail', pattern_id=pattern.id)
    pattern.delete()
    return redirect('posts:patterns_index')