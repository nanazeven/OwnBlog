from django.urls import path
from comments import views
app_name = 'comments'
urlpatterns = [
    path('post/<int:article_id>/',views.post_comment, name='post_comment'),
    path('def/<int:comment_id>/',views.del_comment, name='del_comment'),
    path('page/<int:article_id>/<int:page>/', views.page_comment, name='page_comment'),
]