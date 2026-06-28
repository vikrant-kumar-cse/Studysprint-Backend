from django.urls import path
from .views import DashboardOverviewView, DailyProgressView, WeeklyStatsView

urlpatterns = [
    path('overview/', DashboardOverviewView.as_view(), name='dashboard-overview'),
    path('daily-progress/', DailyProgressView.as_view(), name='daily-progress'),
    path('weekly-stats/', WeeklyStatsView.as_view(), name='weekly-stats'),
]
