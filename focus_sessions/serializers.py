from rest_framework import serializers
from .models import FocusSession
from tasks.models import Task


class FocusSessionSerializer(serializers.ModelSerializer):
    task_title = serializers.CharField(source='task.title', read_only=True, default=None)
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), required=False, allow_null=True)

    class Meta:
        model = FocusSession
        fields = ('id', 'task', 'task_title', 'duration_minutes', 'completed_at', 'created_at')
        read_only_fields = ('id', 'created_at')

    def validate_task(self, task):
        if task is not None:
            request = self.context['request']
            if task.user != request.user:
                raise serializers.ValidationError("Invalid task.")
        return task
