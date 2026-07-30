from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics

from django.contrib.auth.models import User

from .models import Appointment, Department, Doctor, ProblemReport
from .serializers import (
    AppointmentSerializer,
    DepartmentSerializer,
    DoctorSerializer,
    ProblemReportSerializer,
    RegisterSerializer,
)


class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer


@api_view(["GET"])
def current_user(request):

    return Response({
        "username":request.user.username,
        "email":request.user.email

    })


@api_view(["GET"])
def hospital_info(request):
    return Response({
        "name": "PulseNet Hospital",
        "appointment_title": "Book an Appointment",
        "problem_title": "Highlight Your Problems",
    })


class DepartmentListView(generics.ListCreateAPIView):
    queryset = Department.objects.all().order_by("name")
    serializer_class = DepartmentSerializer


class DoctorListView(generics.ListCreateAPIView):
    queryset = Doctor.objects.select_related("department").all().order_by("name")
    serializer_class = DoctorSerializer


class AppointmentListCreateView(generics.ListCreateAPIView):
    queryset = Appointment.objects.select_related(
        "department",
        "doctor",
        "patient",
    ).all().order_by("-created_at")
    serializer_class = AppointmentSerializer


class ProblemReportListCreateView(generics.ListCreateAPIView):
    queryset = ProblemReport.objects.all().order_by("-created_at")
    serializer_class = ProblemReportSerializer
