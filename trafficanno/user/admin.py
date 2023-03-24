from django.contrib import admin
from .models import User, AdvertiserAccount, PublisherAccount


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(AdvertiserAccount)
class AdvertiserAccountAdmin(admin.ModelAdmin):
    pass


@admin.register(PublisherAccount)
class PublisherAccountAdmin(admin.ModelAdmin):
    pass
