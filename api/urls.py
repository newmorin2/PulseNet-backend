from django.urls import path
from .views import (
    RegisterView,
    current_user,
    DepartmentListCreateView,
    DepartmentDetailView,
)

from .views import (
    AppointmentListCreateView,
    DepartmentListView,
    DoctorListView,
    ProblemReportListCreateView,
    RegisterView,
    current_user,
    hospital_info,
)

urlpatterns=[
    path(
        "",
        hospital_info
    ),

urlpatterns = [
    path(
        "signup/",
        RegisterView.as_view(),
    ),

    path(
        "me/",
        current_user
    ),
    path(
        "departments/",
        DepartmentListView.as_view()
    ),
    path(
        "doctors/",
        DoctorListView.as_view()
    ),
    path(
        "appointments/",
        AppointmentListCreateView.as_view()
    ),
    path(
        "problems/",
        ProblemReportListCreateView.as_view()
    )

]
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
