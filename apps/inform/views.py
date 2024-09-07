from rest_framework import viewsets

from apps.inform.models import Inform
from apps.inform.serializers import InformSerializer
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status


class InformViewSet(viewsets.ModelViewSet):
    queryset = Inform.objects.all()
    serializer_class = InformSerializer

    def get_queryset(self):
        queryset = self.queryset.select_related("author").prefetch_related(
            "read", "departments").filter(Q(public=True) | Q(departments=self.request.user.department) | Q(author=self.request.user)
                                         ).distinct()
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author.uuid == self.request.user.uuid:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)