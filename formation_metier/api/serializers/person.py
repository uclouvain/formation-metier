from rest_framework import serializers

from formation_metier.models.person import Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'numberFGS', 'role_formation_metier']
