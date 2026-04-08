import requests
from django.http import HttpResponse

# Shopify App credentials
API_KEY = "fd94453f0bc07974fc189fdd98e7f0b9"
API_SECRET = "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"

# OAuth scopes
SCOPES = "read_products,read_orders,read_customers"

# Redirect URL (must match Shopify dashboard)
REDIRECT_URI = "http://localhost:8000/callback/"


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

    return HttpResponse(f"""
        <h2>Shopify App Install</h2>
        <p>Store: {shop}</p>
        <a href="{install_url}">
            <button style="padding:10px 20px;font-size:16px;">
                Install App
            </button>
        </a>
    """)


def shopify_callback(request):
    shop = request.GET.get("shop")
    code = request.GET.get("code")

    if not shop or not code:
        return HttpResponse("Missing shop or code")

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
        return HttpResponse(f"Error getting token: {data}")

    return HttpResponse(f"""
        <h2>Shopify OAuth Success ✅</h2>
        <p>Store: {shop}</p>
        <p><b>Admin API Access Token:</b></p>
        <pre>{access_token}</pre>
        <p>Save this token in your backend database.</p>
    """)


