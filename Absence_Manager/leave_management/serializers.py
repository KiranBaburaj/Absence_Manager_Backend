from rest_framework import serializers
from .models import  LeaveRequest, LeaveSummary, CalendarEvent

from rest_framework import serializers
from .models import LeaveRequest

class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ['id', 'user', 'leave_type', 'start_date', 'end_date', 'reason', 'status', 'applied_at']
        read_only_fields = ['manager', 'applied_at']  # Make manager and applied_at read-only

        
class LeaveSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveSummary
        fields = ['user', 'annual_leave', 'sick_leave', 'casual_leave', 'maternity_leave']

class CalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarEvent
        fields = ['user', 'title', 'start_date', 'end_date']
