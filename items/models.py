from django.db import models
from django.contrib.auth.models import User 
from categories.models import Category
# Create your models here.

class Item(models.Model):
    #아이템 등록한 사용자 
    owner_user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, related_name="owned_items")
    #아이템이 어떤 카테고리에 속하는지 
    category = models.ForeignKey(Category, null=False, blank=False, on_delete=models.PROTECT, related_name="category_items")
    
    #이름
    product_name = models.CharField(max_length=100)
    #이미지
    image = models.ImageField(upload_to="items/", blank=False, null=False)
    #링크
    product_url = models.CharField(max_length=500, blank=True, null=True)
    #가격 -> 0이상의 정수
    price = models.PositiveIntegerField(blank=True, null=True)
    
    #스크랩 여부 
    is_scrapped = models.BooleanField(default=False)
    #삭제 여부
    is_deleted = models.BooleanField(default=False)

    #등록 날짜, 수정 날짜
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
    
    