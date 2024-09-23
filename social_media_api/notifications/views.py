
from rest_framework import status, generics, permissions, response
from notifications.models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    permission_classes = [generics.IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        # Prioritize unread notifications
        return Notification.objects.filter(recipient=self.request.user).order_by('is_read', '-timestamp')

class MarkNotificationAsReadView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, notification_id):
        notification = generics.get_object_or_404(Notification, id=notification_id, recipient=request.user)

        if notification.is_read:
            return response.Response({"error": "Notification already marked as read."}, status=status.HTTP_400_BAD_REQUEST)

        notification.mark_as_read()
        return response.Response({"success": "Notification marked as read."}, status=status.HTTP_200_OK)
