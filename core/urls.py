from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from .custom_schema import CustomSpectacularAPIView
from drf_spectacular.views import (
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("users.urls")),
    path("", include("organization.urls")),
    path(
        "schema/",
        CustomSpectacularAPIView.as_view(),
        name="schema",
    ),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("redocs/", SpectacularRedocView.as_view(url_name="schema"), name="redocs"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
