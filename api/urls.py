from django.urls import path
from .views import (
    RegisterView,
    current_user,
    DepartmentListCreateView,
    DepartmentDetailView,
)

urlpatterns = [
    path(
        "signup/",
        RegisterView.as_view(),
    ),

    path(
        "me/",
        current_user,
    ),

    path(
        "departments/",
        DepartmentListCreateView.as_view(),
    ),

    path(
        "departments/<int:pk>/",
        DepartmentDetailView.as_view(),
    ),
]