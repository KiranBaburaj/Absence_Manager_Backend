from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,  # Add user id here
                    'username': user.username,
                    'email': user.email,
            
                    'department': user.department.name if user.department else None,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            tokens = serializer.get_tokens(user)
            return Response({
                'refresh': tokens['refresh'],
                'access': tokens['access'],
                'user': {
                    'id': user.id,  # Add user id here
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                    'department': {
                        'id': user.department.id if user.department else None,  # Include department ID
                        'name': user.department.name if user.department else None  # Include department name
                    },
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Department
from .serializers import DepartmentSerializer

class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [AllowAny]  # Allow any user to access this view


from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Department
from .serializers import UserSerializer
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Department
from .serializers import UserSerializer
from rest_framework import status

class EmployeesByDepartmentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, department_id):
        try:
            department = Department.objects.get(id=department_id)
            
            # Check if the authenticated user is the manager of the department
            if not (request.user.is_manager and request.user.department == department):
                return Response({"error": "You do not have permission to view this department's employees."}, 
                                status=status.HTTP_403_FORBIDDEN)

            # Filter employees of this department
            employees = User.objects.filter(department=department, role='employee')
            serializer = UserSerializer(employees, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Department.DoesNotExist:
            return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
