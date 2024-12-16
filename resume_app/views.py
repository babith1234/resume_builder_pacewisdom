import re
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Employee,EmployeeProjectMapping,Project
from .serializers import EmployeeSerializer, EmployeeProjectSerializer, ProjectSerializer
from django.http import HttpResponse
from django.templatetags.static import static


from django.template.loader import render_to_string
from weasyprint import HTML

def home(request):
    return render(request, 'home.html')

def searchEmployee(request):
    return render(request, 'EmployeeSearch.html')

class EmployeeCreateView(APIView):
    def get(self, request, *args, **kwargs):
        # Render the form for GET requests
        return render(request, 'EmployeeDetail.html')
    
    def post(self, request, *args, **kwargs):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Employee created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class CreateProjectAndMapEmployeeView(APIView):

    def get(self, request, *args, **kwargs):
        # Render the form for GET requests
        return render(request, 'projectDetail.html')
    
    def post(self, request, *args, **kwargs):
        # Get employee_id from the request parameters
        employee_id = request.query_params.get('employee_id')

        if not employee_id:
            return Response({"error": "Employee ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the employee exists
        try:
            employee = Employee.objects.get(employee_id=employee_id)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)

        # Create the project
        project_serializer = ProjectSerializer(data=request.data)
        if project_serializer.is_valid():
            project = project_serializer.save()  # Save and get the created project instance

            # Map the employee and project in the EmployeeProject model
            mapping_data = {
                "employee": employee_id,
                "project": project.id,
                "role": request.data.get("role", "Contributor"),  # Default role is "Contributor"
            }
            mapping_serializer = EmployeeProjectSerializer(data=mapping_data)

            if mapping_serializer.is_valid():
                mapping_serializer.save()
                return Response({
                    "message": "Project created and employee mapped successfully.",
                    "project_data": project_serializer.data,
                    "mapping_data": mapping_serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(mapping_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)    



# class EmployeeDetailsView(APIView):
#     def get(self, request, *args, **kwargs):
#         employee_id = request.query_params.get('employee_id')
#         if not employee_id:
#             return Response({"error": "Employee ID is required"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             # Fetch employee details
#             employee = Employee.objects.get(employee_id=employee_id)
#             employee_serializer = EmployeeSerializer(employee)

#             # Fetch associated project IDs
#             project_mappings = EmployeeProjectMapping.objects.filter(employee_id=employee_id)
#             project_ids = project_mappings.values_list('project_id', flat=True)

#             # Fetch project details
#             projects = Project.objects.filter(id__in=project_ids)
#             project_serializer = ProjectSerializer(projects, many=True)

#             header_image_url = request.build_absolute_uri(static('header.png'))

#             # Combine data into context for template rendering
#             context = {
#                 "employee_details": employee_serializer.data,
#                 "projects": project_serializer.data,
#                 "header_image_url": header_image_url
#             }

#             # Render HTML template with data
#             html_string = render_to_string('resume_template.html', context)

#             # Generate PDF from HTML
#             pdf_file = HTML(string=html_string).write_pdf()

#             # Return PDF as HTTP response
#             response = HttpResponse(pdf_file, content_type='application/pdf')
#             response['Content-Disposition'] = 'inline; filename="Employee_Resume.pdf"'
#             return response

#         except Employee.DoesNotExist:
#             return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)



class EmployeeDetailsView(APIView):
    def get(self, request, *args, **kwargs):
        search_query = request.query_params.get('employee_id')  # This can be ID or Name
        
        if not search_query:
            return Response({"error": "Search query is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if the query contains digits (assume it's an employee_id if it does)
            if re.search(r'\d', search_query):
                # Search by employee_id
                employee = Employee.objects.get(employee_id=search_query)
            else:
                # Search by employee_name if no digits are present
                employee = Employee.objects.get(name__iexact=search_query)  # Case-insensitive match
            
            # Serialize employee details
            employee_serializer = EmployeeSerializer(employee)

            # Fetch associated project IDs
            project_mappings = EmployeeProjectMapping.objects.filter(employee_id=employee.employee_id)
            project_ids = project_mappings.values_list('project_id', flat=True)

            # Fetch project details
            projects = Project.objects.filter(id__in=project_ids)
            project_serializer = ProjectSerializer(projects, many=True)

            # Get the static header image URL
            header_image_url = request.build_absolute_uri(static('header.png'))

            # Combine data into context for template rendering
            context = {
                "employee_details": employee_serializer.data,
                "projects": project_serializer.data,
                "header_image_url": header_image_url
            }

            # Render HTML template with data
            html_string = render_to_string('resume_template.html', context)

            # Generate PDF from HTML
            pdf_file = HTML(string=html_string).write_pdf()

            # Return PDF as HTTP response
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="Employee_Resume.pdf"'
            return response

        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
