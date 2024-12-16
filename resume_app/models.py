from django.db import models

class Employee(models.Model):
    employee_id = models.CharField(max_length=50, unique=True,primary_key=True)
    name = models.CharField(max_length=100)
    summary = models.TextField()
    phone_number = models.CharField(max_length=15, unique=True)  
    email = models.EmailField(max_length=255, unique=True)  
    technical_skills = models.JSONField()  

    def __str__(self):
        return f"{self.name} ({self.employee_id})"
    


class Project(models.Model):
    
    project_name = models.CharField(max_length=200) 
    technologies = models.TextField() 
    description = models.TextField() 
    roles_and_responsibilities = models.JSONField()  

    def __str__(self):
        return f"{self.project_name} ({self.id})"
    
class EmployeeProjectMapping(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('employee', 'project')

        

