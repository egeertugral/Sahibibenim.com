from django.shortcuts import render, redirect
from django.contrib.auth import login
from vehicles.models import Vehicle
from comments.models import Comment
from favorites.models import Favorite
from vehicles.forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']  # Emaili manuel kaydet
            user.save()
            login(request, user)
            return redirect('vehicle_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def profile(request):
    my_vehicles = Vehicle.objects.filter(owner=request.user)
    my_comments = Comment.objects.filter(user=request.user).select_related('vehicle')
    my_favorites = Favorite.objects.filter(user=request.user).select_related('vehicle')

    return render(request, 'accounts/profile.html', {
        'my_vehicles': my_vehicles,
        'my_comments': my_comments,
        'my_favorites': my_favorites,
    })