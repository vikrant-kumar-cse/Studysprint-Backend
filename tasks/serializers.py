from rest_framework import serializers
from .models import Task
from subjects.models import Subject


class TaskSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())

    class Meta:
        model = Task
        fields = (
            'id', 'title', 'description', 'subject', 'subject_name',
            'priority', 'due_date', 'is_completed', 'completed_at',
            'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'completed_at', 'created_at', 'updated_at')

    def validate_subject(self, subject):
        # Ensure the subject belongs to the requesting user
        request = self.context['request']
        if subject.user != request.user:
            raise serializers.ValidationError("Invalid subject.")
        return subject
