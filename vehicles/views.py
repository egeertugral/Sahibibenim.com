from django.db import models
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from comments.forms import CommentForm
from comments.models import Comment
from django.views.generic.edit import UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Vehicle
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from favorites.models import Favorite
from .forms import MessageForm
from .forms import VehicleImageFormSet

from .models import VehicleImage
from comments.models import Comment

def profile(request):
    my_vehicles = Vehicle.objects.filter(owner=request.user)
    my_comments = Comment.objects.filter(user=request.user)
    my_favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'profile.html', {
        'my_vehicles': my_vehicles,
        'my_comments': my_comments,
        'my_favorites': my_favorites
    })


def send_message(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    receiver = vehicle.owner  # Aracı kimin eklediğine göre bunu güncelle

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.vehicle = vehicle
            message.save()
            return redirect('vehicle_detail', pk=vehicle.id)
    else:
        form = MessageForm()

    return render(request, 'vehicles/send_message.html', {'form': form, 'vehicle': vehicle})

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.user == request.user:
        comment.delete()
    return redirect('profile')


def toggle_favorite(request, vehicle_id):
    vehicle = Vehicle.objects.get(id=vehicle_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, vehicle=vehicle)
    if not created:
        favorite.delete()
    return redirect('vehicle_detail', pk=vehicle_id)

def my_favorites(request):
    user_favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'favorites/my_favorites.html', {'favorites': user_favorites})

def vehicle_list(request):
    vehicles = Vehicle.objects.all()  # ✅ Bu satır mutlaka başta olacak
    is_for_rent = request.GET.get('is_for_rent')
    if is_for_rent == "true":
        vehicles = vehicles.filter(is_for_rent=True)
    elif is_for_rent == "false":
        vehicles = vehicles.filter(is_for_rent=False)
    search = request.GET.get("search")
    brand = request.GET.get("brand")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    min_year = request.GET.get("min_year")
    max_year = request.GET.get("max_year")
    min_km = request.GET.get("min_km")
    max_km = request.GET.get("max_km")
    fuel_type = request.GET.get("fuel_type")
    transmission = request.GET.get("transmission")
    color = request.GET.get("color")
    min_power = request.GET.get("min_power")
    sunroof = request.GET.get("sunroof")

    if search:
        vehicles = vehicles.filter(model__icontains=search)
    if brand:
        vehicles = vehicles.filter(brand=brand)
    if min_price:
        vehicles = vehicles.filter(price__gte=min_price)
    if max_price:
        vehicles = vehicles.filter(price__lte=max_price)
    if min_year:
        vehicles = vehicles.filter(year__gte=min_year)
    if max_year:
        vehicles = vehicles.filter(year__lte=max_year)
    if min_km:
        vehicles = vehicles.filter(km__gte=min_km)
    if max_km:
        vehicles = vehicles.filter(km__lte=max_km)
    if fuel_type:
        vehicles = vehicles.filter(fuel_type=fuel_type)
    if transmission:
        vehicles = vehicles.filter(transmission=transmission)
    if color:
        vehicles = vehicles.filter(color__icontains=color)
    if min_power:
        vehicles = vehicles.filter(engine_power__gte=min_power)
    if sunroof == "true":
        vehicles = vehicles.filter(sunroof=True)
    elif sunroof == "false":
        vehicles = vehicles.filter(sunroof=False)

    brands = Vehicle.objects.values_list('brand', flat=True).distinct()

    return render(request, 'vehicles/vehicle_list.html', {
        'vehicles': vehicles,
        'brands': brands,
    })

def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    comments = Comment.objects.filter(vehicle=vehicle).order_by('-created_at')
    is_favorited = False

    if request.user.is_authenticated:
        is_favorited = vehicle.favorite_set.filter(user=request.user).exists()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.vehicle = vehicle
            comment.user = request.user
            comment.save()
            return redirect('vehicle_detail', pk=vehicle.pk)
    else:
        form = CommentForm()

    return render(request, 'vehicles/vehicle_detail.html', {
        'vehicle': vehicle,
        'form': form,
        'comments': comments,
        'is_favorited': is_favorited,
    })

class VehicleCreateView(LoginRequiredMixin, CreateView):
    model = Vehicle
    template_name = 'vehicles/vehicle_form.html'
    fields = ['brand', 'model', 'price', 'year', 'km', 'is_for_rent', 'fuel_type',
              'transmission', 'engine_power', 'sunroof', 'color', 'location', 'description']
    success_url = reverse_lazy('vehicle_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['image_formset'] = VehicleImageFormSet(self.request.POST, self.request.FILES)
        else:
            data['image_formset'] = VehicleImageFormSet(queryset=VehicleImage.objects.none())
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        if image_formset.is_valid():
            form.instance.owner = self.request.user
            self.object = form.save()

            for image_form in image_formset:
                if image_form.cleaned_data and not image_form.cleaned_data.get('DELETE', False):
                    image = image_form.save(commit=False)
                    image.vehicle = self.object  # 🔥 GÖRSELLERLE ARACI BAĞLA
                    image.save()
            return redirect('vehicle_detail', pk=self.object.pk)
        else:
            return self.form_invalid(form)



    

class VehicleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Vehicle
    fields = ['brand', 'model', 'price', 'year', 'km', 'is_for_rent', 'fuel_type',
              'transmission', 'engine_power', 'sunroof', 'color', 'location', 'description']
    template_name = 'vehicles/vehicle_form.html'
    success_url = reverse_lazy('vehicle_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().owner == self.request.user





    


class VehicleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Vehicle
    template_name = 'vehicles/vehicle_confirm_delete.html'
    success_url = reverse_lazy('vehicle_list')

    def test_func(self):
        vehicle = self.get_object()
        return self.request.user == vehicle.owner
    
    