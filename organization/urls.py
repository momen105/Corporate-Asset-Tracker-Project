from django.urls import path
from .views import OrganizationView, DeviceView, DeviceDelegateView

urlpatterns = []

only_project_owner_urlpatterns = [
    path(
        "create-organization/",
        OrganizationView.as_view(),
    ),
    path(
        "create-organization/<int:id>/",
        OrganizationView.as_view(),
    ),
]
all_user_urlpatterns = [
    path("create-device/", DeviceView.as_view()),
    path("create-device/<int:id>/", DeviceView.as_view()),
    path("delegate-device/", DeviceDelegateView.as_view()),
    path("delegate-device/<int:id>/", DeviceDelegateView.as_view()),
]

urlpatterns += only_project_owner_urlpatterns
urlpatterns += all_user_urlpatterns
