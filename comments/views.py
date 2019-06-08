from django.shortcuts import render, get_object_or_404, reverse, redirect
from comments.models import Comment
from blog.models import Article
from comments.forms import CommentsForm
from django.http import JsonResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.models import BlogUser
from django.utils import timezone


# Create your views here.

def post_comment(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if not request.user.is_authenticated:
        return JsonResponse({'code': 2, 'message': '你还没有登陆'})

    if request.method == "POST":
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment = form.save(False)
            comment.article = article
            if request.POST['parent'] != '-1':
                parent = Comment.objects.get(id=request.POST['parent'])
                comment.parent = parent
            comment.author = request.user
            comment.save()
            comment.pub_time = timezone.localtime(comment.pub_time)
            res = {
                'code': 1,
                'message': '评论成功',
                'cur_comment': {
                    'cid': comment.id,
                    'ctext': comment.text,
                    'ctime': comment.pub_time.strftime('%Y-%m-%d %H:%M'),
                    'cparent': comment.parent_id,
                    'uid': comment.author.id,
                    'uname': comment.author.username,
                },
            }
            return JsonResponse(res)
        else:
            return JsonResponse({'code': 0, 'message': '数据验证错误，评论失败'})

    return JsonResponse({'code': 0, 'message': 'method错误，评论失败'})


def del_comment(request, comment_id):
    filter_comment = Comment.objects.filter(id=comment_id)
    if len(filter_comment) > 0:
        filter_comment.delete()

    return HttpResponseRedirect(request.path)


def page_comment(request, article_id, page):
    comment_list = Article.objects.filter(id=article_id).first().comment_set.filter(
        parent__isnull=True).order_by('-pub_time')
    paginator = Paginator(comment_list, 5)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果用户请求的页码号不是整数，显示第一页
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果用户请求的页码号超过了最大页码号，显示最后一页
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'comments/comment_list.html', {"contacts": contacts, "curr_article_id": article_id})
