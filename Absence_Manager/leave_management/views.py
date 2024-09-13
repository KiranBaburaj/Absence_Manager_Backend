from rest_framework import viewsets, generics
from .models import LeaveRequest, LeaveSummary, CalendarEvent
from .serializers import LeaveRequestSerializer, LeaveSummarySerializer, CalendarEventSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import LeaveRequest
from .serializers import LeaveRequestSerializer

class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'manager':
            # If the user is a manager, return leave requests from users in their department
            return LeaveRequest.objects.filter(user__department=user.department)
        else:
            # If the user is a regular user, return their leave requests
            return LeaveRequest.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LeaveSummaryViewSet(viewsets.ModelViewSet):
    queryset = LeaveSummary.objects.all()
    serializer_class = LeaveSummarySerializer

    def get_object(self):
        # Ensure only one LeaveSummary per user
        obj, created = LeaveSummary.objects.get_or_create(user=self.request.user)
        return obj

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CalendarEventViewSet(viewsets.ModelViewSet):
    queryset = CalendarEvent.objects.all()
    serializer_class = CalendarEventSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
