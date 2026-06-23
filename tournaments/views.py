from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from categories.models import Category
from items.models import Item
from .models import Tournament, TournamentMatch

# Create your views here.
#코드가 너무 길어서 함수로
def get_round_name(round_no):
    if round_no == 2:
        return "결승"
    return str(round_no) + "강"

def make_pairs(items):
    pairs = []

    for i in range(0, len(items), 2):
        pairs.append([items[i], items[i + 1]])

    return pairs

def get_eliminated_items(tournament):
    matches = TournamentMatch.objects.filter(
        tournament=tournament,
        winner_item__isnull=False
    )

    eliminated_items = []

    for match in matches:
        if match.left_item != match.winner_item:
            eliminated_items.append(match.left_item)

        if match.right_item != match.winner_item:
            eliminated_items.append(match.right_item)

    return eliminated_items

def make_next_round_matches(tournament, winners):
    next_round = tournament.current_round // 2

    tournament.current_round = next_round
    tournament.save()

    match_no = 1

    for i in range(0, len(winners), 2):
        new_match = TournamentMatch()
        new_match.tournament = tournament
        new_match.round_no = next_round
        new_match.match_no = match_no
        new_match.left_item = winners[i]
        new_match.right_item = winners[i + 1]
        new_match.save()

        match_no += 1

#시작
# main
def tournament_main(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    tournaments = Tournament.objects.filter(user=request.user).order_by("-started_at")

    return render(request, "tournaments/cup_start.html", {"tournaments": tournaments})


# create
def tournament_create(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    if request.method == "GET":
        default_categories = Category.objects.filter(is_default=True)
        my_categories = Category.objects.filter(creator=request.user)
        categories = default_categories | my_categories

        return render(request, "tournaments/cup_select.html", {"categories": categories, "size_choices": Tournament.SIZE_CHOICES})

    category_id = request.POST["category"]
    tournament_size = int(request.POST["tournament_size"])
    
    category = get_object_or_404(Category, pk=category_id)

    items = Item.objects.filter(owner_user=request.user, category=category, is_deleted=False)


    # 선택한 N강보다 아이템 수가 적으면 생성 불가
    if items.count() < tournament_size:
        default_categories = Category.objects.filter(is_default=True)
        my_categories = Category.objects.filter(creator=request.user)
        categories = default_categories | my_categories
        return render(request, "tournaments/cup_select.html", {
            "categories": categories,
            "size_choices": Tournament.SIZE_CHOICES,
            "error": f"{tournament_size}강을 진행하려면 {tournament_size}개 이상의 아이템이 필요합니다."
        })

    tournament = Tournament()
    tournament.user = request.user
    tournament.category = category
    tournament.tournament_size = tournament_size
    tournament.current_round = tournament_size
    tournament.save()

    selected_items = list(items.order_by("?")[:tournament_size])

    # 1라운드 
    match_no = 1

    for i in range(0, tournament_size, 2):
        match = TournamentMatch()
        match.tournament = tournament
        match.round_no = tournament_size
        match.match_no = match_no
        match.left_item = selected_items[i]
        match.right_item = selected_items[i + 1]
        match.save()

        match_no += 1

    return redirect("tournaments:play", tournament.id)

# play
def tournament_play(request, pk):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    tournament = get_object_or_404(Tournament, pk=pk, user=request.user)

    if tournament.status == "COMPLETED":
        return redirect("tournaments:result", tournament.id)

    if request.method == "POST":
        match_id = request.POST["match_id"]
        winner_item_id = int(request.POST["winner_item_id"])

        match = get_object_or_404(TournamentMatch, pk=match_id, tournament=tournament, winner_item__isnull=True)

        # 왼쪽 
        if winner_item_id == match.left_item.id:
            match.winner_item = match.left_item
        # 오른쪽 
        elif winner_item_id == match.right_item.id:
            match.winner_item = match.right_item
        else:
            return redirect("tournaments:play", tournament.id)
        
        match.save()

        not_finished_match = TournamentMatch.objects.filter(
            tournament=tournament,
            round_no=tournament.current_round,
            winner_item__isnull=True
        ).first()

        if not_finished_match:
            return redirect("tournaments:play", tournament.id)

        finished_matches = TournamentMatch.objects.filter(
            tournament=tournament,
            round_no=tournament.current_round
        ).order_by("match_no")

        winners = []

        for finished_match in finished_matches:
            winners.append(finished_match.winner_item)

        if len(winners) == 1:
            tournament.status = "COMPLETED"
            tournament.winner_item = winners[0]
            tournament.completed_at = timezone.now()
            tournament.save()

            return redirect("tournaments:result", tournament.id)

        # 다음 라운드 
        make_next_round_matches(tournament, winners)
        return redirect("tournaments:play", tournament.id)

    current_match = TournamentMatch.objects.filter(
        tournament=tournament,
        round_no=tournament.current_round,
        winner_item__isnull=True
    ).order_by("match_no").first()

    if current_match is None:
        return redirect("tournaments:result", tournament.id)

    total_matches = TournamentMatch.objects.filter(
        tournament=tournament,
        round_no=tournament.current_round
    ).count()

    return render(request, "tournaments/cup_ing.html", {
    "tournament": tournament,
    "left_item": current_match.left_item, 
    "right_item": current_match.right_item,
    "match_id": current_match.id,
    "current_match_no": current_match.match_no,
    "total_matches": total_matches,
    "round_name": get_round_name(tournament.current_round)
})


def tournament_result(request, pk):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    tournament = get_object_or_404(Tournament, pk=pk, user=request.user)

    return render(request, "tournaments/cup_result.html", {
        "tournament": tournament,
        "winner_item": tournament.winner_item,
        "eliminated_items": get_eliminated_items(tournament),
    })


# 공유 링크
def tournament_link(request, pk):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    tournament = get_object_or_404(Tournament, pk=pk, user=request.user)

    share_url = request.build_absolute_uri(
        reverse("tournaments:shared_intro", kwargs={"token": tournament.share_token})
    )

    return render(request, "tournaments/cup_link.html", {"tournament": tournament, "share_url": share_url})


# 다시하기
def tournament_restart(request, pk):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    return redirect("tournaments:create")


# 공유 링크 인트로 화면 / 비로그인 허용
def shared_intro(request, token):
    tournament = get_object_or_404(Tournament, share_token=token)
    return render(request, "tournaments/cup_share.html", {
        "tournament": tournament,
        "sharer": tournament.user,
        "winner_item": tournament.winner_item,
    })


# 공유 모아컵 참여 화면 / 비로그인 허용
def shared_play(request, token):
    tournament = get_object_or_404(Tournament, share_token=token)

    session_key = "shared_moco_" + str(token)

    if session_key not in request.session:
        first_matches = TournamentMatch.objects.filter(
            tournament=tournament,
            round_no=tournament.tournament_size
        ).order_by("match_no")

        matches = []

        for match in first_matches:
            matches.append([match.left_item.id, match.right_item.id])

        request.session[session_key] = {
            "round_no": tournament.tournament_size,
            "matches": matches,
            "current_index": 0,
            "winners": [],
            "eliminated_items": [],
            "is_finished": False,
            "winner_item_id": None,
        }

    state = request.session[session_key]

    if state["is_finished"]:
        winner_item = get_object_or_404(Item, pk=state["winner_item_id"])
        eliminated_items = Item.objects.filter(id__in=state["eliminated_items"])

        return render(request, "tournaments/cup_result.html", {
            "tournament": tournament,
            "winner_item": winner_item,
            "eliminated_items": eliminated_items,
            "is_shared": True,
            "share_user": tournament.user,
            "original_winner_item": tournament.winner_item,
        })

    if request.method == "POST":
        winner_item_id = int(request.POST["winner_item_id"])

        current_index = state["current_index"]
        left_item_id = state["matches"][current_index][0]
        right_item_id = state["matches"][current_index][1]

        if winner_item_id == left_item_id:
            state["winners"].append(left_item_id)
            state["eliminated_items"].append(right_item_id)

        elif winner_item_id == right_item_id:
            state["winners"].append(right_item_id)
            state["eliminated_items"].append(left_item_id)

        else:
            return redirect("tournaments:shared_play", token=token)

        state["current_index"] += 1

        # 현재 라운드 경기가 아직 남아있으면 계속 진행
        if state["current_index"] < len(state["matches"]):
            request.session[session_key] = state
            request.session.modified = True
            return redirect("tournaments:shared_play", token=token)

        # 최종 우승자 결정
        if len(state["winners"]) == 1:
            state["is_finished"] = True
            state["winner_item_id"] = state["winners"][0]

            request.session[session_key] = state
            request.session.modified = True

            return redirect("tournaments:shared_play", token=token)

        # 다음 라운드로 넘어가기
        state["round_no"] = state["round_no"] // 2
        state["matches"] = make_pairs(state["winners"])
        state["current_index"] = 0
        state["winners"] = []

        request.session[session_key] = state
        request.session.modified = True

        return redirect("tournaments:shared_play", token=token)

    # 공유 모아컵 진행 화면
    current_index = state["current_index"]
    left_item_id = state["matches"][current_index][0]
    right_item_id = state["matches"][current_index][1]

    left_item = get_object_or_404(Item, pk=left_item_id)
    right_item = get_object_or_404(Item, pk=right_item_id)

    return render(request, "tournaments/cup_ing.html", {
        "tournament": tournament,
        "left_item": left_item,
        "right_item": right_item,
        "total_matches": len(state["matches"]),
        "current_match_no": current_index + 1,
        "round_name": get_round_name(state["round_no"]),
        "is_shared": True,
        "share_user": tournament.user,
    })
    
#mypage 전체보기 구현하기위한 코드 
# 내가 완료한 모아컵 결과 전체 조회
def tournament_record(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    results = Tournament.objects.filter(
        user=request.user,
        status="COMPLETED",
        winner_item__isnull=False
    ).select_related("winner_item", "category").order_by("-completed_at")

    return render(request, "tournaments/cup_record.html", {"results": results})