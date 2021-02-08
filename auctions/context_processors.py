from django.contrib.auth.decorators import login_required

from .models import WatchList



def watch_list_count(request):
    nb_items = 0
    if request.user.is_authenticated:
        watched_list = WatchList.objects.filter(author=request.user)
        nb_items = len(watched_list)
    return {
        "nb_items": nb_items
        }

