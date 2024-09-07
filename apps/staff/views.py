from rest_framework.generics import ListAPIView
from apps.oaauther.serializers import DepartmentSerializer
from apps.oaauther.models import OADepartment


class DepartmentList(ListAPIView):
    queryset = OADepartment.objects.all()
    serializer_class = DepartmentSerializer
