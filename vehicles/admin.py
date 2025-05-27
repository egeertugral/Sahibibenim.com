from django.contrib import admin
from .models import Vehicle
from .models import Message
from .models import VehicleImage


class VehicleImageInline(admin.TabularInline):  # veya StackedInline
    model = VehicleImage
    extra = 5

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'price', 'year', 'is_for_rent', 'owner')
    search_fields = ('brand', 'model')
    list_filter = ('is_for_rent', 'year')
    inlines = [VehicleImageInline]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'vehicle', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'vehicle__brand')