from django.contrib import admin
from django.contrib.auth.models import User, Group

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("external_id", "first_name","username", "attempt", "referrals", "last_date")
    list_filter = ("first_name","username", "attempt", "referrals")
    fields = ("first_name","username", "attempt")


admin.site.unregister(User)
admin.site.unregister(Group)
