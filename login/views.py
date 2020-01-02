from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .form import UserForm
from .form import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def user_login(request):
    if request.session.get('is_login', None):
        return redirect('/blog')
    if request.method == "GET":
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
    if request.method == "POST":
        login_form = UserForm(request.POST)
        if login_form.is_valid():
            if User.objects.filter(username=login_form.cleaned_data['username']):
                user = authenticate(username=login_form.cleaned_data['username'],
                                    password=login_form.cleaned_data['password'])
                if user:
                    login(request, user)
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.username
                    if request.session.get('login_from', None) == '/':
                        return redirect('/blog')
                    else:
                        return HttpResponseRedirect(request.session.get('login_from', None))
                else:
                    message = "密码不正确！"
            else:
                message = "用户不存在！"
        return render(request, 'login/login.html', locals())
    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def user_logout(request):
    # 没登录也就没退出这说
    if not request.session.get('is_login', None):
        return redirect('/blog')
    logout(request)
    request.session.flush()
    return redirect("blog:index")


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect('/blog')
    if request.method == "POST":
        register_form = RegisterForm(data=request.POST)
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同!"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = User.objects.filter(username=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名!'
                    return render(request, 'login/register.html', locals())
                same_email_user = User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱!'
                    return render(request, 'login/register.html', locals())
                # 当一切都OK的情况下，创建新用户
                new_user = register_form.save(commit=False)
                new_user.set_password(register_form.cleaned_data['password1'])
                new_user.username = register_form.cleaned_data['username']
                new_user.email = register_form.cleaned_data['email']
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
        message = '验证码错误!'
        return render(request, 'login/register.html', locals())
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())
