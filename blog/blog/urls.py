"""django_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views
app_name = 'blog'
urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    path('', views.article_list, name='list'),
    path('article/<int:article_id>.html', views.detail, name='detail'),
    path('archives/<int:year>/',views.year_archives, name='year_archives'),
    path('archives/<int:year>/<int:month>/',views.mouth_archives, name='month_archives'),
    path('tag/<str:tag_name>.html',views.tag_article, name='tag'),
]
