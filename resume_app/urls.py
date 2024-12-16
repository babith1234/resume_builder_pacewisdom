from django.urls import path
from .views import EmployeeCreateView, CreateProjectAndMapEmployeeView, EmployeeDetailsView,home,searchEmployee
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home,name='home'),
    path('search/',searchEmployee),
    path('employee/create/', EmployeeCreateView.as_view(), name='employee-create'),
    path('project/create/', CreateProjectAndMapEmployeeView.as_view(), name='project-create'),
    path('resume/', EmployeeDetailsView.as_view(), name='resume'),
    
]+ static(settings.STATIC_URL,document_root=settings.STATIC_ROOT) 

