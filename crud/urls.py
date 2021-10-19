from django.urls import path
from . import views

app_name = 'crud'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('<int:board_id>/', views.detail, name='detail'),
    path('board/create/', views.board_create, name='board_create'),
    path('board/modify/<int:board_id>/', views.board_modify, name='board_modify'),
    path('board/delete/<int:board_id>/', views.board_delete, name='board_delete'),
]