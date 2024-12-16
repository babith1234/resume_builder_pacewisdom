from rest_framework import serializers
from .models import Employee, Project,EmployeeProjectMapping

class EmployeeSerializer(serializers.ModelSerializer):
    technical_skills = serializers.JSONField()
    class Meta:
        model = Employee
        fields = ['employee_id', 'name', 'summary', 'phone_number', 'email', 'technical_skills']


class ProjectSerializer(serializers.ModelSerializer):
        roles_and_responsibilities = serializers.JSONField()
        class Meta:
            model = Project
            fields = ['id', 'project_name', 'technologies', 'description', 'roles_and_responsibilities']

class EmployeeProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProjectMapping
        fields = ['employee', 'project']        
