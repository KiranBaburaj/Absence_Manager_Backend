from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeaveRequestViewSet, LeaveSummaryViewSet, CalendarEventViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'leave-requests', LeaveRequestViewSet)
router.register(r'leave-summaries', LeaveSummaryViewSet)
router.register(r'calendar-events', CalendarEventViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('api/', include(router.urls)),
]
