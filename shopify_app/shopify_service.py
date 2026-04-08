import requests
from .models import ShopifyStore


def get_products():

    store = ShopifyStore.objects.first()

    if not store:
        return []

    url = f"https://{store.shop_domain}/admin/api/2024-01/products.json"

    headers = {

        "X-Shopify-Access-Token": store.access_token
    }

    response = requests.get(url, headers=headers)

    data = response.json()

    return data.get("products", [])