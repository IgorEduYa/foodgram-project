from rest_framework import mixins, status, viewsets
from rest_framework.response import Response


class CreateDestroyViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return Response({"success": True}, status=status.HTTP_201_CREATED)

