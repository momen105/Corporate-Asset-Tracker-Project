from django.urls import path
from .views import OrganizationView

urlpatterns = []

project_owner_urlpatterns = [
    path(
        "create-organization/",
        OrganizationView.as_view(),
    ),
    path(
        "create-organization/<int:org_id>/",
        OrganizationView.as_view(),
    ),
]
urlpatterns += project_owner_urlpatterns