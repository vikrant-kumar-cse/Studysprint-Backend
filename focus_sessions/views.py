from rest_framework import viewsets, permissions
from .models import FocusSession
from .serializers import FocusSessionSerializer


class FocusSessionViewSet(viewsets.ModelViewSet):
    """
    Save and list completed Pomodoro focus sessions.
    POST /api/sessions/   -> save a completed session {task, duration_minutes, completed_at}
    GET  /api/sessions/   -> list this user's sessions (most recent first)
    """
    serializer_class = FocusSessionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return FocusSession.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
