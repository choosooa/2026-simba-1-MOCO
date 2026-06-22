from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import ProtectedError
from .models import Category

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

        return redirect('items:storage')  # 수정 필요
        
def delete(request, category_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    delete_category = get_object_or_404(Category, pk=category_id)

    # 기본 카테고리 삭제 불가
    if delete_category.is_default:
        return redirect('items:storage')  # 수정 필요

    # 본인 카테고리 아니면 막음
    if delete_category.creator != request.user:
        return redirect('items:storage')  # 수정 필요

    # 아이템 있으면 삭제 불가
    try:
        delete_category.delete()
    except ProtectedError:
        return redirect('items:storage')  # 수정 필요

    return redirect('items:storage')  # 수정 필요