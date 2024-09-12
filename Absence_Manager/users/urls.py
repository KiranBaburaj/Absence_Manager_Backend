from django.urls import path
from .views import DepartmentListCreateView, EmployeesByDepartmentView, RegisterView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
     path('departments/', DepartmentListCreateView.as_view(), name='department-list-create'),
        path('departments/<int:department_id>/employees/', EmployeesByDepartmentView.as_view(), name='employees-by-department'),
]


