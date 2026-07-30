from django.urls import path

from .views import (
    RegisterView,
    appointment_history_view,
    appointments_view,
    care_team_view,
    current_user,
    departments_view,
    profile_view,
    upcoming_appointments_view,
)

urlpatterns = [
    path("signup/", RegisterView.as_view(), name="signup"),
    path("me/", current_user, name="me"),
    path("profile/", profile_view, name="profile"),
    path("departments/", departments_view, name="departments"),
    path("care-team/", care_team_view, name="care-team"),
    path("appointments/", appointments_view, name="appointments"),
    path("appointments/upcoming/", upcoming_appointments_view, name="appointments-upcoming"),
    path("appointments/history/", appointment_history_view, name="appointments-history"),
]