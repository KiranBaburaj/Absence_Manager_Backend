from django.db import models
from django.conf import settings
from users.models import User

class LeaveSummary(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leave_summary')
    annual_leave = models.IntegerField(default=0)
    sick_leave = models.IntegerField(default=0)
    casual_leave = models.IntegerField(default=0)
    maternity_leave = models.IntegerField(default=0)

    def __str__(self):
        return f"Leave Summary for {self.user.username}"


class CalendarEvent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.title} ({self.start_date} to {self.end_date})"


class LeaveRequest(models.Model):
    LEAVE_TYPE_CHOICES = (
        ('annual', 'Annual Leave'),
        ('sick', 'Sick Leave'),
        ('casual', 'Casual Leave'),
        ('maternity', 'Maternity Leave'),
    )
    
    LEAVE_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=LEAVE_STATUS_CHOICES, default='pending')
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='approved_leaves')
    applied_at = models.DateTimeField(auto_now_add=True)
    
    # New relationships
    leave_summary = models.ForeignKey(LeaveSummary, on_delete=models.CASCADE, null=True, blank=True, related_name='leave_requests')
    calendar_event = models.OneToOneField(CalendarEvent, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.leave_type} ({self.start_date} to {self.end_date})"

    @property
    def duration(self):
        return (self.end_date - self.start_date).days + 1

    def save(self, *args, **kwargs):
        # Get the previous status of the leave request
        previous_status = None
        if self.pk:  # Check if the object already exists
            previous_instance = LeaveRequest.objects.get(pk=self.pk)
            previous_status = previous_instance.status

        # Automatically set the manager based on the user's department
        if not self.manager:
            if self.user.department:
                try:
                    self.manager = User.objects.get(department=self.user.department, role='manager')
                except User.DoesNotExist:
                    self.manager = None  # No manager found

        # Check if the leave is being approved and handle leave summary and calendar event
        if self.status == 'approved':
            # Update the leave summary for the user
            leave_summary, created = LeaveSummary.objects.get_or_create(user=self.user)
            if self.leave_type == 'annual':
                leave_summary.annual_leave += self.duration
            elif self.leave_type == 'sick':
                leave_summary.sick_leave += self.duration
            elif self.leave_type == 'casual':
                leave_summary.casual_leave += self.duration
            elif self.leave_type == 'maternity':
                leave_summary.maternity_leave += self.duration
            leave_summary.save()
            self.leave_summary = leave_summary  # Link leave summary to leave request

            # Create or update a calendar event for the approved leave
            if not self.calendar_event:
                self.calendar_event = CalendarEvent.objects.create(
                    user=self.user,
                    title=f"{self.leave_type.capitalize()} Leave",
                    start_date=self.start_date,
                    end_date=self.end_date
                )
            else:
                # Update the existing calendar event if needed
                self.calendar_event.start_date = self.start_date
                self.calendar_event.end_date = self.end_date
                self.calendar_event.save()

        # Handle case where the status changes from approved to rejected
        if previous_status == 'approved' and self.status == 'rejected':
            # Revert the leave summary
            if self.leave_summary:
                if self.leave_type == 'annual':
                    self.leave_summary.annual_leave -= self.duration
                elif self.leave_type == 'sick':
                    self.leave_summary.sick_leave -= self.duration
                elif self.leave_type == 'casual':
                    self.leave_summary.casual_leave -= self.duration
                elif self.leave_type == 'maternity':
                    self.leave_summary.maternity_leave -= self.duration
                self.leave_summary.save()

            # Delete the associated calendar event
            if self.calendar_event:
                self.calendar_event.delete()
                self.calendar_event = None  # Reset the calendar event field

        super().save(*args, **kwargs)

    
    def delete(self, *args, **kwargs):
        # Explicitly delete related calendar events and leave summary
        if self.calendar_event:
            self.calendar_event.delete()
        if self.leave_summary and not self.leave_summary.leave_requests.exists():
            self.leave_summary.delete()
        super().delete(*args, **kwargs)
