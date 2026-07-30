from rest_framework import status
from rest_framework.test import APITestCase

from .models import Appointment, Department, ProblemReport


class PulseNetApiTests(APITestCase):
    def test_can_book_appointment(self):
        department = Department.objects.create(
            name="Cardiology",
            description="Heart and blood vessel care",
        )

        response = self.client.post(
            "/api/appointments/",
            {
                "full_name": "Jane Patient",
                "email": "jane@example.com",
                "phone": "+254700000000",
                "department": department.id,
                "date": "2026-08-15",
                "additional_notes": "Chest discomfort in the morning",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 1)
        self.assertEqual(Appointment.objects.first().full_name, "Jane Patient")

    def test_can_submit_problem_report(self):
        response = self.client.post(
            "/api/problems/",
            {
                "name": "John Patient",
                "email": "john@example.com",
                "symptoms": "Dizziness and previous surgery history",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProblemReport.objects.count(), 1)
        self.assertEqual(ProblemReport.objects.first().status, "New")
