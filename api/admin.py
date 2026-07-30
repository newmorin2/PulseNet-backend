from django.contrib import admin

# Register your models here.
from .models import Appointment, Department, Doctor, ProblemReport

admin.site.register(Department)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(ProblemReport)
