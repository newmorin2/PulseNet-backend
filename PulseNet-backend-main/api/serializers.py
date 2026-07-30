from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Appointment, Department, Doctor, PatientProfile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        PatientProfile.objects.get_or_create(user=user)
        return user


class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = ["phone", "address", "date_of_birth", "emergency_contact"]


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name", "description"]


class DoctorSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = ["id", "name", "specialization", "experience", "bio", "department"]


class AppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ["id", "doctor", "date", "time", "reason", "status", "created_at"]
        read_only_fields = ["status", "created_at"]

    def create(self, validated_data):
        request = self.context.get("request")
        doctor = validated_data["doctor"]
        patient = request.user
        return Appointment.objects.create(patient=patient, doctor=doctor, **validated_data)


class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["doctor", "date", "time", "reason"]

    def create(self, validated_data):
        request = self.context.get("request")
        patient = request.user
        return Appointment.objects.create(patient=patient, **validated_data)
