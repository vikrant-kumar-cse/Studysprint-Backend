from datetime import timedelta

from django.utils import timezone
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.models import Task
from focus_sessions.models import FocusSession
from focus_sessions.serializers import FocusSessionSerializer


class DashboardOverviewView(APIView):
    """
    GET /api/dashboard/overview/
    Returns: total_focus_minutes, completed_tasks_count, total_tasks_count,
             pending_tasks_count, recent_sessions (last 5)
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        sessions = FocusSession.objects.filter(user=user)
        tasks = Task.objects.filter(user=user)

        total_focus_minutes = sessions.aggregate(total=Sum('duration_minutes'))['total'] or 0
        completed_tasks_count = tasks.filter(is_completed=True).count()
        total_tasks_count = tasks.count()
        pending_tasks_count = total_tasks_count - completed_tasks_count

        recent_sessions = sessions.order_by('-completed_at')[:5]

        return Response({
            'total_focus_minutes': total_focus_minutes,
            'total_focus_hours': round(total_focus_minutes / 60, 2),
            'completed_tasks_count': completed_tasks_count,
            'total_tasks_count': total_tasks_count,
            'pending_tasks_count': pending_tasks_count,
            'recent_sessions': FocusSessionSerializer(recent_sessions, many=True, context={'request': request}).data,
        })


class DailyProgressView(APIView):
    """
    GET /api/dashboard/daily-progress/?days=7
    Returns per-day focus minutes and session counts for the last N days (default 7).
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        days = int(request.query_params.get('days', 7))
        since = timezone.now() - timedelta(days=days - 1)

        sessions = (
            FocusSession.objects.filter(user=request.user, completed_at__gte=since)
            .annotate(day=TruncDate('completed_at'))
            .values('day')
            .annotate(total_minutes=Sum('duration_minutes'), session_count=Count('id'))
            .order_by('day')
        )

        # Build a complete date range so days with zero sessions still show up
        data_by_day = {str(item['day']): item for item in sessions}
        result = []
        for i in range(days):
            day = (since + timedelta(days=i)).date()
            day_str = str(day)
            entry = data_by_day.get(day_str)
            result.append({
                'date': day_str,
                'total_minutes': entry['total_minutes'] if entry else 0,
                'session_count': entry['session_count'] if entry else 0,
            })

        return Response(result)


class WeeklyStatsView(APIView):
    """
    GET /api/dashboard/weekly-stats/
    Returns total focus minutes, session count, and tasks completed for the
    last 7 days, plus a daily breakdown (handy for Recharts bar/line charts).
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        since = timezone.now() - timedelta(days=6)

        sessions = FocusSession.objects.filter(user=user, completed_at__gte=since)
        total_minutes = sessions.aggregate(total=Sum('duration_minutes'))['total'] or 0
        session_count = sessions.count()

        tasks_completed = Task.objects.filter(
            user=user, is_completed=True, completed_at__gte=since
        ).count()

        daily = (
            sessions.annotate(day=TruncDate('completed_at'))
            .values('day')
            .annotate(total_minutes=Sum('duration_minutes'))
            .order_by('day')
        )

        return Response({
            'week_total_minutes': total_minutes,
            'week_total_hours': round(total_minutes / 60, 2),
            'week_session_count': session_count,
            'week_tasks_completed': tasks_completed,
            'daily_breakdown': list(daily),
        })
