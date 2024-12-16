from django.contrib import admin

# Register your models here.
from resume_app.models import Employee, EmployeeProjectMapping, Project

admin.site.register(Employee)
admin.site.register(EmployeeProjectMapping)
admin.site.register(Project)
