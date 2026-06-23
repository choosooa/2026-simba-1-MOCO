from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Profile
import random

from items.models import Item
from tournaments.models import Tournament

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('items:main')  # 로그인 성공 → 메인으로
        else:
            return render(request, 'accounts/login.html', {'error': '아이디 또는 비밀번호가 올바르지 않습니다.'})

    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    return redirect('accounts:login')


def signup(request):
    if request.method == 'POST':
        errors = {}

        username = request.POST['username']
        password = request.POST['password']

        # 아이디 형식
        if len(username) < 4 or len(username) > 15:
            errors['username'] = '4자~15자 영문또는 숫자만 가능합니다.'
        else:
            for char in username:
                if not ('a' <= char <= 'z' or 'A' <= char <= 'Z' or char.isdigit()):
                    errors['username'] = '4자~15자 영문또는 숫자만 가능합니다.'
                    break

        # 아이디 중복
        if not errors.get('username') and User.objects.filter(username=username).exists():
            errors['username'] = '이미 사용중인 아이디입니다.'

        # 비밀번호 형식
        if len(password) < 8:
            errors['password'] = '영문, 숫자, 특수문자를 조합하여 입력해주세요.'
        else:
            has_alpha = has_digit = has_special = False
            for char in password:
                if 'a' <= char <= 'z' or 'A' <= char <= 'Z':
                    has_alpha = True
                elif char.isdigit():
                    has_digit = True
                elif char in '!@#$%^&*?':
                    has_special = True
            if not (has_alpha and has_digit and has_special):
                errors['password'] = '영문, 숫자, 특수문자를 조합하여 입력해주세요.'

        # 비밀번호 불일치
        if password != request.POST['confirm']:
            errors['confirm'] = '비밀번호가 일치하지 않습니다.'

        # 닉네임 중복
        if Profile.objects.filter(nickname=request.POST['nickname']).exists():
            errors['nickname'] = '이미 사용중인 닉네임입니다.'

        if errors:
            return render(request, 'accounts/signup.html', {'error': errors})

        new_user = User.objects.create_user(username=username, password=password)
        profile = new_user.profile
        profile.nickname = request.POST['nickname']
        profile.is_terms_agreed = True
        profile.save()
        auth.login(request, new_user)
        return redirect('items:main')

    return render(request, 'accounts/signup.html')

def terms_detail(request):
    return render(request, 'accounts/terms.html')

QUOTES = [
    "마음이 가는 것과 실제로 사고 싶은 것은 다를 수도 있어 ",
    "충동구매보다 더 좋은 건 나에게 정말 필요한 걸 찾는 거야!",
    "무엇을 살지 고민하는 것도 똑똑한 소비의 시작이야 💡",
    "항상 사고 싶은 걸 다 살 수는 없어! 그래서 우리는 선택을 해. 지금 가장 갖고 싶은 단 하나를 찾아보자 ✨",
]


#mypage 구현 함수 
def mypage(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login') ##이걸 주석처리 하시면 로그인 안 한 사용자도 가능해요 
    
    nickname = request.user.profile.nickname
    quote = random.choice(QUOTES)
    
    recent_results = Tournament.objects.filter(
        user=request.user,
        status='COMPLETED',
        winner_item__isnull=False
    ).select_related('winner_item').order_by('-completed_at')[:2]
    
    return render(request, 'accounts/mypage.html', {
        'nickname': nickname, 'quote': quote, 'recent_results': recent_results})