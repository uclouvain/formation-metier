from rest_framework import serializers

from formation_metier.models.employe_uclouvain import EmployeUCLouvain


class EmployeUCLSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeUCLouvain
        fields = ['id', 'name', 'number_fgs', 'role_formation_metier']
