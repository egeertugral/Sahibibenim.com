from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'user', 'created_at')
    search_fields = ('user__username', 'vehicle__model')
