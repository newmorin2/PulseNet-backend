from django.db import models

# Create your models here.
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
        on_delete=models.CASCADE
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE
    )

    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Pending"
    )

    def __str__(self):

        return f"{self.patient.username} - {self.doctor.name}"