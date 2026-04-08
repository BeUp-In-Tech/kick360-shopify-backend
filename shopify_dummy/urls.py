# from django.contrib import admin
# from django.urls import path, include

# from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi


# schema_view = get_schema_view(
#     openapi.Info(
#         title="Shopify Integration API",
#         default_version='v1',
#         description="Shopify backend service",
#     ),
#     public=True,
#     permission_classes=[permissions.AllowAny],
# )


# urlpatterns = [

#     path('admin/', admin.site.urls),

#     path('', include('shopify_app.urls')),

#     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),

# ]

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# ✅ Root test endpoint
def home(request):
    return HttpResponse("Kick360 Backend is Live 🚀")


schema_view = get_schema_view(
    openapi.Info(
        title="Shopify Integration API",
        default_version='v1',
        description="Shopify backend service",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [

    # ✅ ROOT FIX (this was missing)
    path('', home),

    path('admin/', admin.site.urls),

    # your app routes
    path('', include('shopify_app.urls')),

    # swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),

    # ✅ docs (you didn’t have this)
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0)),
]