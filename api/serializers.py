from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Department

from .models import Appointment, Department, Doctor, ProblemReport


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:

        model = User
        fields = [
            "username",
            "email",
            "password"
        ]


    def create(self, validated_data):
        user = User.objects.create_user(

            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]

        )

        return user


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            "id",
            "name",
            "description",
        ]


class DoctorSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = [
            "id",
            "department",
            "name",
            "specialization",
            "experience",
        ]


class AppointmentSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "id",
            "full_name",
            "email",
            "phone",
            "department",
            "department_name",
            "doctor",
            "date",
            "time",
            "reason",
            "additional_notes",
            "status",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "created_at",
        ]

    def validate(self, attrs):
        if not attrs.get("reason") and attrs.get("additional_notes"):
            attrs["reason"] = attrs["additional_notes"]
        return attrs


class ProblemReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemReport
        fields = [
            "id",
            "name",
            "email",
            "symptoms",
            "status",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "created_at",
        ]
class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = "__all__"
