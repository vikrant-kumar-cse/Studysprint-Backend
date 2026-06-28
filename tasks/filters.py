import django_filters
from .models import Task


class TaskFilter(django_filters.FilterSet):
    subject = django_filters.NumberFilter(field_name='subject_id')
    priority = django_filters.CharFilter(field_name='priority')
    is_completed = django_filters.BooleanFilter(field_name='is_completed')
    due_date = django_filters.DateFilter(field_name='due_date')
    due_before = django_filters.DateFilter(field_name='due_date', lookup_expr='lte')
    due_after = django_filters.DateFilter(field_name='due_date', lookup_expr='gte')

    class Meta:
        model = Task
        fields = ['subject', 'priority', 'is_completed', 'due_date']
