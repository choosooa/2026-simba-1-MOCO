from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import ProtectedError
from .models import Category
from items.models import Item

def create(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    if request.method == 'POST':
        if Category.objects.filter(creator=request.user, name=request.POST['name']).exists():
            return render(request, 'categories/create.html', {'error': '동일 이름의 카테고리가 존재합니다.'})
        new_category = Category()
        new_category.creator = request.user
        new_category.name = request.POST['name']   
        new_category.save()
        return redirect('items:plus')
    
    return render(request, 'categories/create.html')

def delete(request, category_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    delete_category = get_object_or_404(Category, pk=category_id)

    if delete_category.is_default:
        return redirect('items:plus')

    if delete_category.creator != request.user:
        return redirect('items:plus')

    try:
        delete_category.delete()
    except ProtectedError:
        return redirect('items:plus')

    return redirect('items:plus')

def edit(request, category_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    edit_category = get_object_or_404(Category, pk=category_id)
    
    if edit_category.creator != request.user:
        return redirect('items:plus')
    
    if edit_category.is_default:
        return redirect('items:plus')
    
    if request.method == 'POST':
        new_name = request.POST.get('name')
        if new_name:
            if Category.objects.filter(creator=request.user, name=new_name).exists():
                return redirect('items:plus')
            edit_category.name = new_name
            edit_category.save()
        return redirect('items:plus')
    
    return render(request, 'categories/edit.html', {'category': edit_category})

#current 함수 추가 
def current(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
     #닉네임
    nickname = request.user.profile.nickname
    #전체 아이템 개수 
    total_items_count = Item.objects.filter(owner_user=request.user, is_deleted=False).count()
    #기본 카테고리 
    default_categories = Category.objects.filter(is_default=True)
    #내가 만든 카테고리 
    my_categories = Category.objects.filter(creator=request.user)
    
    categories = []

    # 기본 카테고리 별 개수 세기 
    for category in default_categories:
        category.item_count = Item.objects.filter(
            owner_user=request.user, category=category, is_deleted=False).count()
        categories.append(category)

    # 내가 만든 카테고리별 개수 세기
    for category in my_categories:
        category.item_count = Item.objects.filter(
            owner_user=request.user, category=category, is_deleted=False).count()
        categories.append(category)
        
    # 편집 모드인지 확인
    is_edit = False
    if request.GET.get('edit') == '1':
        is_edit = True 

    return render(request, 'categories/current.html', {
        'nickname': nickname,
        'total_items_count': total_items_count,
        'categories': categories,
        'is_edit': is_edit
    })