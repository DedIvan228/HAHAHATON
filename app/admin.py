from django.contrib import admin
from .models import Rool

@admin.register(Rool)
class RoomRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'role')
    list_filter = ('room', 'role')
