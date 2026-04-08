
# Register your models here.
from django.contrib import admin
from .models import AccessCode, ShopifyStore


@admin.register(AccessCode)
class AccessCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "order_id", "email", "email_sent")
    search_fields = ("email", "code", "order_id")
    list_filter = ("email_sent",)


@admin.register(ShopifyStore)
class ShopifyStoreAdmin(admin.ModelAdmin):
    list_display = ("shop_domain", "access_token")