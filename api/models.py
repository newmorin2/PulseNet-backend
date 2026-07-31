from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    head = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    image = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Doctor(models.Model):

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="doctors"
    )
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    experience = models.IntegerField()

    def __str__(self):
        return self.name


class Appointment(models.Model):
    STATUS = (
        ("Pending","Pending"),
        ("Approved","Approved"),
        ("Cancelled","Cancelled"),
    )
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        related_name="appointments",
        null=True,
        blank=True
    )
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    reason = models.TextField(blank=True)
    additional_notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        appointment_date = self.date.isoformat() if self.date else "unscheduled"
        return f"{self.full_name} - {appointment_date}"


class ProblemReport(models.Model):
    STATUS = (
        ("New", "New"),
        ("Reviewed", "Reviewed"),
        ("Closed", "Closed"),
    )
    name = models.CharField(max_length=120)
    email = models.EmailField()
    symptoms = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS, default="New")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.status}"
