from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import CreateOrganizationAdminView, AddEmployeeView

urlpatterns = []

all_user_urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

only_project_owner_urlpatterns = [
    path(
        "create-organization-admin/",
        CreateOrganizationAdminView.as_view(),
    ),
]

organization_admin_and_employee_urlpatterns = [
    path("add-employee/", AddEmployeeView.as_view()),
    path("add-employee/<int:id>/", AddEmployeeView.as_view()),
]


urlpatterns += all_user_urlpatterns
urlpatterns += only_project_owner_urlpatterns
urlpatterns += organization_admin_and_employee_urlpatterns
