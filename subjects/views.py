from rest_framework import viewsets, permissions
from .models import Subject
from .serializers import SubjectSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for Subjects, scoped to the logged-in user.
    GET /api/subjects/         -> list
    POST /api/subjects/        -> create
    GET /api/subjects/{id}/    -> retrieve
    PUT/PATCH /api/subjects/{id}/ -> update
    DELETE /api/subjects/{id}/ -> delete
    """
    serializer_class = SubjectSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Subject.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
