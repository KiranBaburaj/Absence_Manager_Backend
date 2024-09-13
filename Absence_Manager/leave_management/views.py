from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import LeaveRequest, LeaveSummary, CalendarEvent
from .serializers import LeaveRequestSerializer, LeaveSummarySerializer, CalendarEventSerializer

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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'manager':
            # If the user is a manager, return leave summaries from users in their department
            return LeaveSummary.objects.filter(user__department=user.department)
        else:
            # If the user is a regular user, return their leave summary
            return LeaveSummary.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CalendarEventViewSet(viewsets.ModelViewSet):
    queryset = CalendarEvent.objects.all()
    serializer_class = CalendarEventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'manager':
            # If the user is a manager, return calendar events from users in their department
            return CalendarEvent.objects.filter(user__department=user.department)
        else:
            # If the user is a regular user, return their calendar events
            return CalendarEvent.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)