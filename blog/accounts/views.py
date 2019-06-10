from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from accounts.models import BlogUser
from accounts.forms import LoginForm, RegisterForm, PasswordChangeForm
from django.contrib import auth


# Create your views here.

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # 自动判断模块  可以判断你提交的信息是不是和user表中的内容是否相同
            user = auth.authenticate(username=username, password=password)

            if user:
                # autho.login() 这一步相当于设置session的值
                auth.login(request, user)
                return JsonResponse({'code': 1, 'message': 'Login Success'})
            else:
                return JsonResponse({"code": 0, 'message': "Wrong password."})
        else:
            return JsonResponse({'code': 0, 'message': 'Wrong password. Please try again.'})
    else:
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']

            # 自动save 不需要手动save
            new_user = BlogUser.objects.create_user(username, email, password)
            return JsonResponse({'code': 1, 'message': 'Register Success'})
            # return HttpResponseRedirect("/accounts/login/")

        else:
            print(form.error_class)
            return JsonResponse({'code': 0, 'message': 'Register Fail. Please try again.', 'form': form.errors})
            # return render(request, 'accounts/registration.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'accounts/registration.html', {'form': form})


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return HttpResponseRedirect('/')
    return JsonResponse({'code': 0, 'message': 'error'})


def profile(request, user_id):
    if not request.user.is_authenticated:
        return JsonResponse({'code': 0, "message": "error"})
    get_object_or_404(BlogUser, id=user_id)
    return JsonResponse({"code": 1})


def password_change(request, user_id):
    if not request.user.is_authenticated:
        return JsonResponse({'code': 0, "message": "error"})
    curr_user = get_object_or_404(BlogUser, id=user_id)
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('old_username')
            username = curr_user.username
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                new_password = form.cleaned_data.get('password2')
                user.set_password(new_password)
                user.save()
                return JsonResponse({'code': 1, 'message': 'Password Change Success'})
            else:
                return render(request, 'accounts/password_change.html', {'form': form})
    else:
        form = PasswordChangeForm()
        return render(request, 'accounts/password_change.html', {'form': form})
