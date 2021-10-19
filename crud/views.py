from django.core.paginator import Paginator
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

from django.http import HttpResponse
from .models import Board
from .forms import BoardForm

def index(request):
    # 게시판 목록 출력하기
    page = request.GET.get('page', '1') # 페이지

    board_list = Board.objects.order_by('-create_date')

    # 페이징 처리
    paginator = Paginator(board_list, 10)
    page_obj = paginator.get_page(page)

    context = {'board_list' : page_obj}

    return render(request, 'crud/board_list.html', context)

def detail(request, board_id):
    # 게시판 조회
    board = Board.objects.get(id=board_id)
    context = {'board':board}
    return render(request, 'crud/board_detail.html', context)

@login_required(login_url='common:login')
def board_create(request):
    # 게시판 생성
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.author = request.user
            board.create_date = timezone.now()
            board.save()
            return redirect('crud:index')
    else:
        form = BoardForm()
    context = {'form':form}
    return render(request, 'crud/board_form.html', context)

@login_required(login_url='common:login')
def board_modify(request, board_id):
    # 게시판 수정
    board = get_object_or_404(Board, pk=board_id)
    if request.user != board.author:
        messages.error(request, '수정권한이 없어요 ㅠ,ㅠ')
        return redirect('crud:detail', board_id=board.id)
    if request.method == "POST":
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            board = form.save(commit=False)
            board.author = request.user
            board.modify_date = timezone.now()
            board.save()
            return redirect('crud:detail', board_id=board.id)
    else:
        form = BoardForm(instance=board)
    context = {'form' : form}
    return render(request, 'crud/board_form.html', context)

@login_required(login_url='common:login')
def board_delete(request, board_id):
    # 게시판 삭제
    board = get_object_or_404(Board, pk=board_id)
    if request.user != board.author:
        messages.error(request, '삭제권한이 없어요 ㅠ,ㅠ')
        return render('crud:detail', board_id=board.id)
    board.delete()
    return redirect('crud:index')