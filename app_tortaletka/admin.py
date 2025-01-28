from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("external_id", "last_name", "first_name","username", "attempt")
    list_filter = ("last_name", "first_name","username", "attempt")
    fields = ("last_name", "first_name","username", "attempt")
