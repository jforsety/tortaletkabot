from django.contrib import admin
from django.contrib.auth.models import User, Group

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("external_id", "first_name","username", "attempt", "last_date")
    list_filter = ("first_name","username", "attempt")
    fields = ("first_name","username", "attempt")


admin.site.unregister(User)
admin.site.unregister(Group)
