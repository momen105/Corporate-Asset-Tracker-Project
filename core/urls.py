from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("users.urls")),
    path("", include("organization.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
