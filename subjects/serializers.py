from rest_framework import serializers
from .models import Subject


class SubjectSerializer(serializers.ModelSerializer):
    task_count = serializers.IntegerField(source='tasks.count', read_only=True)

    class Meta:
        model = Subject
        fields = ('id', 'name', 'color', 'description', 'task_count', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
