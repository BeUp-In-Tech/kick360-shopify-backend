from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponseRedirect, HttpResponse
import requests

from .models import AccessCode, ShopifyStore
from .shopify_service import get_products
from .utils import generate_access_code


API_KEY = "fd94453f0bc07974fc189fdd98e7f0b9"
API_SECRET = "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"

SCOPES = "read_products,read_orders,read_customers"

REDIRECT_URI = "https://demiurgic-obumbrant-brooklyn.ngrok-free.dev/callback/"


def shopify_home(request):

    shop = request.GET.get("shop")

    if not shop:
        return HttpResponse("Missing shop parameter")

    install_url = (
        f"https://{shop}/admin/oauth/authorize"
        f"?client_id={API_KEY}"
        f"&scope={SCOPES}"
        f"&redirect_uri={REDIRECT_URI}"
    )

    return HttpResponseRedirect(install_url)


def shopify_callback(request):

    shop = request.GET.get("shop")
    code = request.GET.get("code")

    token_url = f"https://{shop}/admin/oauth/access_token"

    payload = {
        "client_id": API_KEY,
        "client_secret": API_SECRET,
        "code": code,
    }

    response = requests.post(token_url, json=payload)

    data = response.json()

    access_token = data.get("access_token")

    if not access_token:
        return HttpResponse("Error getting access token")

    ShopifyStore.objects.update_or_create(
        shop_domain=shop,
        defaults={"access_token": access_token}
    )

    return HttpResponse(
        f"Shopify store connected successfully ✅ <br> Store: {shop}"
    )


@api_view(["GET"])
def products_api(request):

    products = get_products()

    return Response(products)


@api_view(["GET"])
def access_codes(request):

    email = request.GET.get("email")

    if email:
        codes = AccessCode.objects.filter(email=email)
    else:
        codes = AccessCode.objects.all()   

    result = []

    for c in codes:
        # result.append({
        #     "code": c.code,
        #     "order_id": c.order_id,
        #     "email": c.email
        # })
        result.append({
    "code": c.code,
    "order_id": c.order_id,
    "email": c.email,
    "status": "sent" if c.email_sent else "not_sent"
})

    return Response(result)