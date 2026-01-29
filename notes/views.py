from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Note


def note_list(request):
    notes = Note.objects.all()
    return render(request, 'notes/note_list.html', {'notes': notes})

@login_required
def like_note(request, note_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    note = get_object_or_404(Note, pk=note_id)

    if note.likes.filter(id=request.user.id).exists():
        note.likes.remove(request.user)
        liked = False
    else:
        note.likes.add(request.user)
        liked = True

    total_likes = note.total_likes()

    # Отправляем обновление всем через Redis
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'note_{note_id}',  # группа Redis
        {
            'type': 'like_update',
            'likes': total_likes
        }
    )

    return JsonResponse({'likes': total_likes, 'liked': liked})