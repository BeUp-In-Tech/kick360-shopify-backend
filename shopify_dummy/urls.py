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


# ✅ ROOT TEST
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

    # ✅ root
    path('', home),

    path('admin/', admin.site.urls),

    # ✅ API ROUTES (VERY IMPORTANT PATH CHANGE)
    path('api/', include('shopify_app.urls')),

    # ✅ swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),

    # ✅ redoc
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0)),
]