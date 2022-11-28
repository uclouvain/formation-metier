from formation_metier.models.employe_uclouvain import EmployeUCLouvain
from formation_metier.api.serializers.employe_uclouvain import EmployeUCLSerializer
from rest_framework import generics


class EmployeUCLList(generics.ListAPIView):
    queryset = EmployeUCLouvain.objects.all()
    serializer_class = EmployeUCLSerializer


class EmployeUCLDetail(generics.RetrieveAPIView):
    queryset = EmployeUCLouvain.objects.all()
    serializer_class = EmployeUCLSerializer
