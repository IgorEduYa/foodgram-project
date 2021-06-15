from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status


class CreateDestroyViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return Response({"success": True}, status=status.HTTP_201_CREATED)

