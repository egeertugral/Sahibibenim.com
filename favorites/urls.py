from django.urls import path
from vehicles import views

urlpatterns = [
    path('<int:pk>/toggle/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.my_favorites, name='my_favorites'),
]
