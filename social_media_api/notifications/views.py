from rest_framework.generics import ListAPIView, get_object_or_404,GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from notifications.models import Notification
from .serializers import NotificationSerializer

class NotificationListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        # Prioritize unread notifications
        return Notification.objects.filter(recipient=self.request.user).order_by('is_read', '-timestamp')

class MarkNotificationAsReadView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, notification_id):
        notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)

        if notification.is_read:
            return Response({"error": "Notification already marked as read."}, status=status.HTTP_400_BAD_REQUEST)

        notification.mark_as_read()
        return Response({"success": "Notification marked as read."}, status=status.HTTP_200_OK)
