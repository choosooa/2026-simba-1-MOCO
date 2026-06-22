from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Profile


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('accounts:login')  # 나중에 수정
        else:
            return render(request, 'accounts/login.html')
    
    elif request.method == 'GET':
        return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    return redirect('accounts:login')

def signup(request):
    if request.method == 'POST':

        if request.POST['password'] != request.POST['confirm']:
            return render(request, 'accounts/signup.html', {'error': '비밀번호가 일치하지 않습니다.'})
        
        username = request.POST['username']

        if len(username) < 4 or len(username) > 15:
            return render(request, 'accounts/signup.html', {'error': '4자~15자 영문또는 숫자만 가능합니다.'})

        for char in username:
            if not ('a' <= char <= 'z' or 'A' <= char <= 'Z' or char.isdigit()):
                return render(request, 'accounts/signup.html', {'error': '4자~15자 영문또는 숫자만 가능합니다.'})
    
        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/signup.html', {'error': '이미 사용중인 아이디입니다.'})
        
        password = request.POST['password']

        if len(password) < 8:
            return render(request, 'accounts/signup.html', {'error': '영문, 숫자, 특수문자(?,!,*등)을 조합하여 입력해주세요.'})

        has_alpha = False
        has_digit = False
        has_special = False

        for char in password:
            if 'a' <= char <= 'z' or 'A' <= char <= 'Z':
                has_alpha = True
            elif char.isdigit():
                has_digit = True
            elif char in '!@#$%^&*?':
                has_special = True

        if not (has_alpha and has_digit and has_special):
            return render(request, 'accounts/signup.html', {'error': '영문, 숫자, 특수문자(?,!,*등)을 조합하여 입력해주세요.'})
        
        if Profile.objects.filter(nickname=request.POST['nickname']).exists():
            return render(request, 'accounts/signup.html', {'error': '이미 사용중인 닉네임입니다.'})

        new_user = User.objects.create_user(
            username=username,
            password=password,
        )
        
        profile = new_user.profile
        profile.nickname = request.POST['nickname']
        profile.is_terms_agreed = True
        profile.save()

        auth.login(request, new_user)
        return redirect('accounts:login')  # 나중에 수정
    
    return render(request, 'accounts/signup.html')

def terms_detail(request):
    return render(request, 'accounts/terms.html')