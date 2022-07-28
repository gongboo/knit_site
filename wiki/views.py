from django.shortcuts import render, redirect, get_object_or_404
from .models import WikiPost
from .forms import WikiPostForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from simple_history.models import HistoricalRecords

# Create your views here.



def wiki_post_index(request):
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')  # 검색어
    wikiPosts = WikiPost.objects.order_by('name')
    if kw:
        wikiPosts = wikiPosts.filter(
            Q(name__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw)   # 내용 검색
        ).distinct()
    paginator = Paginator(wikiPosts, 50)
    page_obj = paginator.get_page(page)
    context = {'wikiPosts': page_obj, 'page': page, 'kw': kw}
    return render(request, 'wiki/wiki_index.html', context)


@login_required(login_url='common:login')
def wiki_post_create(request):
    if request.method == "POST":
        form = WikiPostForm(request.POST)

        if form.is_valid():
            wikiPost = form.save(commit = False)
            wikiPost.changed_by = request.user #앗 작성자 업ㅆ음 수정하기
            wikiPost.save()
            return redirect('wiki:wiki_post_index')
    else:
        form = WikiPostForm()
    context={'form': form}
    return render(request, 'wiki/wiki_post_create.html', context)


def wiki_post_detail(request, wiki_post_name):
    wikiPost = WikiPost.objects.get(name=wiki_post_name)


    context = {'wikiPost': wikiPost}
    return render(request, 'wiki/wiki_post_detail.html', context)



@login_required(login_url='common:login')
def wiki_post_modify(request, wiki_post_name):
    wikiPost = get_object_or_404(WikiPost, name=wiki_post_name)

    if request.method == "POST":
        form = WikiPostForm(request.POST, instance=wikiPost)
        if form.is_valid():
            wikiPost = form.save(commit=False)
            wikiPost.modify_date = timezone.now()  # 수정일시 저장
            wikiPost.changed_by = request.user
            wikiPost.save()
            return redirect('wiki:wiki_post_detail', wiki_post_name=wikiPost.name)
    else:
        form = WikiPostForm(instance=wikiPost)
    context = {'form': form}
    return render(request, 'wiki/wiki_post_create.html', context)


# @login_required(login_url='common:login')
# def wiki_post_delete(request, wiki_post_name):
#     wikiPost = get_object_or_404(WikiPost, name=wiki_post_name)
#     wikiPost.delete()
#     return redirect('wiki:wiki_post_index')

def wiki_post_history(request, wiki_post_name):

    wikiPost = WikiPost.objects.get(name=wiki_post_name)
    context = {'wikiPost': wikiPost}
    return render(request, 'wiki/wiki_post_history.html', context)


def wiki_post_history_detail(request, wiki_post_name, wiki_history_id):
    wikiPost = WikiPost.objects.get(name=wiki_post_name)
    #history=HistoricalRecords.objects.get(history_id=wiki_post_name)
    #history=HistoricalRecords.history_id(wiki_history_id)
    #history=wikiPost.history.filter(history_id=wiki_history_id).first()
    #history=wikiPost.history.first()
    #history=HistoricalRecords.filter(history_id=wiki_history_id)
    #print(history._instanceize)
    history=wikiPost.history.get(history_id=wiki_history_id)
    text=""

    if (history.prev_record!=None):
        delta = history.diff_against(history.prev_record)
        for change in delta.changes:
            text+="{} changed from {} to {}".format(change.field, change.old, change.new)

    context = {'text': text,'wikiPost': wikiPost,'history':history}
    return render(request, 'wiki/wiki_post_history_detail.html', context)


def wiki_post_history_revert(request, wiki_post_name, wiki_history_id):
    wikiPost = WikiPost.objects.get(name=wiki_post_name)
    history=wikiPost.history.get(history_id=wiki_history_id)
    history.instance.save()
    context = {'wikiPost': wikiPost}
    return render(request, 'wiki/wiki_post_history.html', context)