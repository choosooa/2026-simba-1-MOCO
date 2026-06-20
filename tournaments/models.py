from django.db import models
from django.contrib.auth.models import User
from categories.models import Category
from items.models import Item 
import uuid 

# Create your models here.
class Tournament(models.Model):
    #토너먼트 크기 선택값
    SIZE_CHOICES = [
        (16,"16강"),
        (32,"32강"),
        (64,"64강"),
    ]
    
    #토너먼즈 진행 상태값
    STATUS_CHOICES = [
        ("IN_PROGRESS","진행중"),
        ("COMPLETED","완료"),
    ]
    
    # 토너먼트하는 사용자
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    # 토너먼트 카테고리
    category = models.ForeignKey(Category, null=False, blank=False, on_delete=models.CASCADE)
    
    #몇 강인지 
    tournament_size = models.PositiveIntegerField(choices=SIZE_CHOICES)
    #토너먼트 상태 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="IN_PROGRESS")
    
    #현재 진행 중인 라운드 
    current_round = models.PositiveIntegerField()
    #최종 우승 아이템 
    winner_item = models.ForeignKey(Item, null=True, blank=True, on_delete=models.SET_NULL)
    
    #시작 시간
    started_at = models.DateTimeField(auto_now_add=True)
    #완료 시간
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.tournament_size}강 - {self.status}"
    
    
class TournamentMatch(models.Model):
    #이 매치가 속한 토너먼트 
    tournament = models.ForeignKey(Tournament, null=False, blank=False, on_delete=models.CASCADE)
    #몇 라운드인지 
    round_no = models.PositiveIntegerField()
    #해당 라운드 안에서 몇 번째 경기인지
    match_no = models.PositiveIntegerField()
    
    #왼쪽 후보 아이템
    left_item = models.ForeignKey(Item, null=False, blank=False, on_delete=models.PROTECT, related_name="left_matches")
    #오른쪽 후보 아이템 
    right_item = models.ForeignKey(Item, null=False, blank=False, on_delete=models.PROTECT, related_name="right_matches")
    #해당 매치의 승리 아이템 
    winner_item = models.ForeignKey(Item, null=True, blank=True, on_delete=models.PROTECT, related_name="won_matches")
    
    #생성 시간
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.tournament} / {self.round_no}강 / {self.match_no}번 매치"
    
class TournamentShare(models.Model):
    #공유할 토너먼트 
    tournament = models.ForeignKey(Tournament, null=False, blank=False, on_delete=models.CASCADE)
    #공유 링크를 만든 유저
    create_user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    
    #공유 - 지피티도움..
    share_token = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    
    #생성 시간
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.create_user.username}의 공유 토너먼트"