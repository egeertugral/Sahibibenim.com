# vehicles/urls.py
from django.urls import path
from vehicles import views
from .views import VehicleCreateView
from .views import VehicleUpdateView, VehicleDeleteView

urlpatterns = [
    path('', views.vehicle_list, name='vehicle_list'),
    path('<int:pk>/', views.vehicle_detail, name='vehicle_detail'),
    path('add/', VehicleCreateView.as_view(), name='vehicle_add'),
    path('<int:pk>/edit/', VehicleUpdateView.as_view(), name='vehicle_edit'),
    path('<int:pk>/delete/', VehicleDeleteView.as_view(), name='vehicle_delete'),
    path('toggle-favorite/<int:vehicle_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.my_favorites, name='my_favorites'),
   path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('<int:vehicle_id>/message/', views.send_message, name='send_message'),
]
