from django.db import models
from django.contrib.auth.models import User
from tasks.models import Task


class FocusSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='focus_sessions')
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True, related_name='focus_sessions')
    duration_minutes = models.PositiveIntegerField(help_text="Duration of the focus session in minutes")
    completed_at = models.DateTimeField(help_text="When the session was completed")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-completed_at']

    def __str__(self):
        return f"{self.user.username} - {self.duration_minutes}min - {self.completed_at}"
