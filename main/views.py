from django.shortcuts import render, get_object_or_404, redirect
from tournaments.models import Tournament, TournamentMatch

def cup_start(request):
    return render(request, 'cup_start.html')

def cup_select(request):
    return render(request, 'cup_select.html')

def cup_ing(request):
    context = {}
    shared_tournament_id = request.session.get('shared_tournament_id')
    if shared_tournament_id:
        try:
            shared_tournament = Tournament.objects.get(id=shared_tournament_id)
            matches = (
                TournamentMatch.objects
                .filter(tournament=shared_tournament)
                .order_by('round_no', 'match_no')
                .select_related('left_item', 'right_item')
            )
            context['shared_tournament'] = shared_tournament
            context['matches'] = matches
        except Tournament.DoesNotExist:
            pass
    return render(request, 'cup_ing.html', context)

def cup_result(request):
  context = {}
    shared_tournament_id = request.session.get('shared_tournament_id')
    if shared_tournament_id:
        try:
            shared_tournament = Tournament.objects.get(id=shared_tournament_id)
            context['is_shared'] = True
            context['sharer'] = shared_tournament.user
            context['sharer_winner'] = shared_tournament.winner_item
        except Tournament.DoesNotExist:
            pass
    return render(request, 'cup_result.html', context)

def login(request):
    return render(request, 'login.html')

def main(request):
    return render(request, 'main.html')

def signup(request):
    return render(request, 'signup.html')

def agree(request):
    return render(request, 'agree.html')

def product(request):
    return render(request, 'product.html')

def plus(request):
    return render(request, 'plus.html')

def plus_info(request):
    return render(request, 'plus_info.html')

def cup_link(request):
    return render(request, 'cup_link.html')

def cup_share(request, share_token):
    tournament = get_object_or_404(Tournament, share_token=share_token)
    return render(request, 'cup_share.html', {
        'tournament': tournament,
        'sharer': tournament.user,
        'winner_item': tournament.winner_item,
    })

def cup_share_start(request, share_token):
    if share_token == 'preview':
        return redirect('cup_result_preview')
    tournament = get_object_or_404(Tournament, share_token=share_token)
    request.session['shared_tournament_id'] = tournament.id
    return redirect('cup_ing')

def cup_share_preview(request):
    """DB 없이 공유 화면 UI를 테스트하기 위한 개발용 뷰"""
    class FakeItem:
        product_name = '나이키 덩크 로우'
        price = 139000

    class FakeUser:
        username = '수아'

    return render(request, 'cup_share.html', {
        'tournament': type('T', (), {'share_token': 'preview'})(),
        'sharer': FakeUser(),
        'winner_item': FakeItem(),
    })

def cup_result_preview(request):
    """DB 없이 공유 결과 화면 UI를 테스트하기 위한 개발용 뷰"""
    class FakeItem:
        product_name = '나이키 덩크 로우'
        price = 139000

    class FakeUser:
        username = '수아'

    return render(request, 'cup_result.html', {
        'is_shared': True,
        'sharer': FakeUser(),
        'sharer_winner': FakeItem(),
    })
