from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from vehicles.models import Vehicle
from .models import Favorite
from django.shortcuts import render

@login_required
def toggle_favorite(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, vehicle=vehicle)
    if not created:
        favorite.delete()  # varsa kaldır
    return redirect('vehicle_detail', pk=pk)


def favorites_list(request):
    user_favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'favorites/favorites_list.html', {'favorites': user_favorites})