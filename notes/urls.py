from django.urls import path
from . import views

urlpatterns = [
    path('', views.note_list, name='note_list'),
    path('like_note/<int:note_id>/', views.like_note, name='like_note'),
]
