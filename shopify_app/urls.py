from django.urls import path

from .views import (
    shopify_home,
    shopify_callback,
    products_api,
    access_codes
)

from .webhooks import order_paid_webhook


urlpatterns = [

    path('install/', shopify_home),

    path('callback/', shopify_callback),

    path('api/products/', products_api),

    path('api/access-codes/', access_codes),

    path('webhooks/order-paid/', order_paid_webhook),
]