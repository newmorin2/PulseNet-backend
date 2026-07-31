from datetime import date, time, timedelta

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Appointment, Department, Doctor, PatientProfile


class PatientPortalApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="patient1",
            email="patient1@example.com",
            password="strongpass123",
        )
        self.department = Department.objects.create(
            name="Cardiology",
            description="Heart care services",
        )
        self.doctor = Doctor.objects.create(
            department=self.department,
            name="Dr. Ada",
            specialization="Cardiology",
            experience=12,
        )

    def test_signup_creates_patient_profile(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newpatient",
                "email": "newpatient@example.com",
                "password": "securepass123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username="newpatient")
        self.assertTrue(PatientProfile.objects.filter(user=user).exists())

    def test_authenticated_patient_can_manage_profile_and_appointments(self):
        self.client.force_authenticate(self.user)

        profile = PatientProfile.objects.get(user=self.user)
        profile.phone = "0712345678"
        profile.save(update_fields=["phone"])

        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["phone"], "0712345678")

        patch_response = self.client.patch(
            reverse("profile"),
            {"phone": "0711111111", "address": "Nairobi"},
            format="json",
        )
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.json()["phone"], "0711111111")

        appointment_response = self.client.post(
            reverse("appointments"),
            {
                "doctor": self.doctor.id,
                "date": (date.today() + timedelta(days=2)).isoformat(),
                "time": time(10, 30).isoformat(),
                "reason": "Chest pain evaluation",
            },
            format="json",
        )
        self.assertEqual(appointment_response.status_code, status.HTTP_201_CREATED)

        upcoming_response = self.client.get(reverse("appointments-upcoming"))
        self.assertEqual(upcoming_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(upcoming_response.json()), 1)

        past_appointment = Appointment.objects.create(
            patient=self.user,
            doctor=self.doctor,
            date=date.today() - timedelta(days=3),
            time=time(9, 0),
            reason="Previous visit",
            status="Approved",
        )
        history_response = self.client.get(reverse("appointments-history"))
        self.assertEqual(history_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(history_response.json()), 1)
        self.assertEqual(history_response.json()[0]["id"], past_appointment.id)

    def test_departments_and_care_team_endpoints_are_public(self):
        response = self.client.get(reverse("departments"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.json()), 1)

        care_team_response = self.client.get(reverse("care-team"))
        self.assertEqual(care_team_response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(care_team_response.json()), 1)
