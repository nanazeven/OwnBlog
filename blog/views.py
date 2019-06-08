from django.shortcuts import render

# Create your views here.
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.conf import settings
from blog.models import Article, Tag
from django.utils.html import strip_tags
from django.shortcuts import get_list_or_404
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import markdown


class IndexView(ListView):
    template_name = "blog/index.html"
    context_object_name = 'article_list'
    model = Article


def article_list(request):
    a_list = Article.objects.all().order_by('-pub_time')
    # for article in a_list:
    #     article.body = md.convert(article.body)
    #     article.body = strip_tags(article.body)[:300]
    cut_md_article(a_list)
    right_archives = get_archives()
    return render(request, 'blog/index.html',
                  context={'tags': Tag.objects.all(), 'article_list': a_list, 'archives': right_archives})


def detail(request, article_id):
    article_detail = Article.objects.filter(id=article_id).first()
    article_detail.viewd()
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    article_detail.body = md.convert(article_detail.body)
    comment_list = article_detail.comment_set.filter(parent__isnull=True).order_by('-pub_time')
    paginator = Paginator(comment_list, 5)
    contacts = paginator.page(1)

    content = {
        'tags': Tag.objects.all(),
        'article': article_detail,
        "toc": md.toc_tokens,
        # 'comment_list': comment_list,
        'contacts':contacts,
        "curr_article_id": article_id,
    }
    return render(request, 'blog/detail.html', context=content)


def year_archives(request, year):
    year_article = Article.objects.filter(pub_time__year=year).order_by('-pub_time')
    # for article in year_article:
    #     article.body = md.convert(article.body)
    #     article.body = strip_tags(article.body)[:300]
    cut_md_article(year_article)
    right_archives = get_archives()
    return render(request, 'blog/index.html',
                  context={'tags': Tag.objects.all(), 'article_list': year_article, 'archives': right_archives})


def mouth_archives(request, year, month):
    month_article = Article.objects.filter(pub_time__year=year, pub_time__month=month).order_by('-pub_time')
    cut_md_article(month_article)
    right_archives = get_archives()
    return render(request, 'blog/index.html',
                  context={'tags': Tag.objects.all(), 'article_list': month_article, 'archives': right_archives})


def tag_article(request, tag_name):
    articles_tags = Tag.objects.get(name=tag_name).article_set.all()
    cut_md_article(articles_tags)
    return render(request, 'blog/index.html',
                  context={'tags': Tag.objects.all(), 'article_list': articles_tags, 'archives': get_archives()})


def get_archives():
    article_list = Article.objects.all().order_by("pub_time")
    res = {}
    for article in article_list:
        article.pub_time = timezone.localtime(article.pub_time)
        year = article.pub_time.year
        month = article.pub_time.month
        if year not in res.keys():
            res[year] = {month: 1}
        elif month not in res[year].keys():
            res[year][month] = 1
        else:
            res[year][month] += 1
    return res


def cut_md_article(article_list):
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    for article in article_list:
        article.body = md.convert(article.body)
        article.body = strip_tags(article.body)[:100]
