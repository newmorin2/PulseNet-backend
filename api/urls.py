from django.urls import path
from .views import (
    RegisterView,
    current_user,
    DepartmentListCreateView,
    DepartmentDetailView,
    AppointmentListCreateView,
    DepartmentListView,
    DoctorListView,
    ProblemReportListCreateView,
    hospital_info,
)

urlpatterns = [
    path(
        "",
        hospital_info,
    ),
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
        DepartmentListView.as_view(),
    ),
    path(
        "doctors/",
        DoctorListView.as_view(),
    ),
    path(
        "appointments/",
        AppointmentListCreateView.as_view(),
    ),
    path(
        "problems/",
        ProblemReportListCreateView.as_view(),
    ),
    path(
        "departments/<int:pk>/",
        DepartmentDetailView.as_view(),
    ),
]
