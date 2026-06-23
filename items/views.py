from django.shortcuts import render, redirect, get_object_or_404
from .models import Item
from categories.models import Category
from django.utils import timezone

def storage(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    categories = Category.objects.filter(creator=request.user) | Category.objects.filter(is_default=True)
    
    category_id = request.GET.get('category')
    if category_id:
        items = Item.objects.filter(owner_user=request.user, category_id=category_id, is_deleted=False)
    else:
        items = Item.objects.filter(owner_user=request.user, is_deleted=False)
    
    return render(request, 'items/storage.html', {'items': items, 'categories': categories})

def search(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    keyword = request.GET.get('q') # 프론트 확인 후 수정 필요
    items = Item.objects.filter(owner_user=request.user, product_name__icontains=keyword, is_deleted=False)
                                                        # 장고 ORM icontains 사용
    return render(request, 'items/storage.html', {'items': items})

def create(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    #수아-수정본
    if request.method == 'POST':
        category_id = request.POST.get('category')
        
        if not category_id:
            return redirect('items:plus')
    
        new_item = Item()
        new_item.owner_user = request.user
        new_item.category = get_object_or_404(Category, pk=request.POST['category'])
        new_item.product_name = request.POST['product_name']
        new_item.image = request.FILES.get('image')
        new_item.product_url = request.POST.get('product_url')
        price = request.POST.get('price')
        if price == '':
            price = None
        new_item.price = price
        new_item.save()
        
        return redirect('items:storage')
    
    return redirect('items:plus')
    #아이템 등록 페이지 처음 보여줄 때 사용/
    #categories = Category.objects.filter(creator=request.user) | Category.objects.filter(is_default=True)
    #return render(request, 'items/create.html', {'categories': categories})

def detail(request, item_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    item = get_object_or_404(Item, pk=item_id)
    
    if item.owner_user != request.user:
        return redirect('items:storage')
    
    return render(request, 'items/detail.html', {'item': item})

def edit(request, item_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    edit_item = get_object_or_404(Item, pk=item_id)
    
    if edit_item.owner_user != request.user:
        return redirect('items:detail', edit_item.id)
    
    if request.method == 'POST':
        edit_item.category = get_object_or_404(Category, pk=request.POST['category'])
        edit_item.product_name = request.POST['product_name']
        edit_item.save()
        return redirect('items:detail', edit_item.id)
    
    categories = Category.objects.filter(creator=request.user) | Category.objects.filter(is_default=True)
    return render(request, 'items/edit.html', {'item': edit_item, 'categories': categories})

def scrap(request, item_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    item = get_object_or_404(Item, pk=item_id)
    
    if item.owner_user != request.user:
        return redirect('items:storage')
    
    item.is_scrapped = not item.is_scrapped
    item.save()
    
    return redirect('items:detail', item.id)

def scrapped_list(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    items = Item.objects.filter(owner_user=request.user, is_scrapped=True, is_deleted=False)
    return render(request, 'items/scrapped_list.html', {'items': items})

def delete(request, item_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    delete_item = get_object_or_404(Item, pk=item_id)
    
    if delete_item.owner_user != request.user:
        return redirect('items:detail', delete_item.id)
    
    delete_item.is_deleted = True
    delete_item.save()
    
    return redirect('items:storage')

def main(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    items = Item.objects.filter(
        owner_user=request.user,
        is_deleted=False
    ).order_by('-created_at')

    recent_items = items[:3]

    today_count = Item.objects.filter(
        owner_user=request.user,
        is_deleted=False,
        created_at__date=timezone.localdate()
    ).count()

    return render(request, 'items/main.html', {
        'items': items,
        'recent_items': recent_items,
        'today_count': today_count,
        'nickname': request.user.profile.nickname,
    })

def plus(request):
    return render(request, 'items/plus.html')

def plus_info(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    categories = Category.objects.filter(creator=request.user) | Category.objects.filter(is_default=True)

    return render(request, 'items/plus_info.html', {'categories': categories})

def product(request):
    return render(request, 'items/product.html')

def main(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    recent_items = Item.objects.filter(
        owner_user=request.user,
        is_deleted=False
    ).order_by('-created_at')[:3]
    
    return render(request, 'items/main.html', {
        'recent_items': recent_items,
        'nickname': request.user.profile.nickname,
    })

def plus(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    categories = Category.objects.filter(creator=request.user) | Category.objects.filter(is_default=True)
    return render(request, 'items/plus.html', {'categories': categories})