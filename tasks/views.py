from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer
from .filters import TaskFilter


class TaskViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for Tasks, scoped to the logged-in user.
    Supports filtering via query params, e.g.:
      /api/tasks/?subject=2&priority=high&is_completed=false&due_date=2026-06-30
    Plus a custom action to mark a task complete:
      POST /api/tasks/{id}/complete/
    """
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filterset_class = TaskFilter

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        task = self.get_object()
        task.is_completed = True
        task.completed_at = timezone.now()
        task.save()
        return Response(self.get_serializer(task).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def uncomplete(self, request, pk=None):
        task = self.get_object()
        task.is_completed = False
        task.completed_at = None
        task.save()
        return Response(self.get_serializer(task).data, status=status.HTTP_200_OK)
