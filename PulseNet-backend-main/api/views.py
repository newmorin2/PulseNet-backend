from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Appointment, Department, Doctor, PatientProfile
from .serializers import (
    AppointmentCreateSerializer,
    AppointmentSerializer,
    DepartmentSerializer,
    DoctorSerializer,
    PatientProfileSerializer,
    RegisterSerializer,
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    profile = request.user.patient_profile
    return Response({
        "username": request.user.username,
        "email": request.user.email,
        "profile": PatientProfileSerializer(profile).data,
    })


@api_view(["GET", "PATCH"])
@permission_classes([permissions.IsAuthenticated])
def profile_view(request):
    profile, _ = PatientProfile.objects.get_or_create(user=request.user)
    if request.method == "PATCH":
        serializer = PatientProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    return Response(PatientProfileSerializer(profile).data)


@api_view(["GET"])
def departments_view(request):
    departments = Department.objects.all().prefetch_related("doctors")
    serializer = DepartmentSerializer(departments, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def care_team_view(request):
    doctors = Doctor.objects.select_related("department").all()
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([permissions.IsAuthenticated])
def appointments_view(request):
    if request.method == "POST":
        serializer = AppointmentCreateSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        appointment = serializer.save()
        return Response(AppointmentSerializer(appointment).data, status=201)

    appointments = Appointment.objects.filter(patient=request.user).select_related("doctor", "doctor__department").order_by("date", "time")
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def upcoming_appointments_view(request):
    today = timezone.now().date()
    appointments = Appointment.objects.filter(
        patient=request.user,
        date__gte=today,
    ).select_related("doctor", "doctor__department").order_by("date", "time")
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def appointment_history_view(request):
    today = timezone.now().date()
    appointments = Appointment.objects.filter(
        patient=request.user,
        date__lt=today,
    ).select_related("doctor", "doctor__department").order_by("-date", "-time")
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)