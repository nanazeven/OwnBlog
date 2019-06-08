from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/',views.logout, name='logout'),
    path('<int:user_id>/profile/', views.profile, name='profile'),
    path('<int:user_id>/pwd_change/', views.password_change, name='pwd_change'),
]