from rest_framework import serializers
from .models import BioData
class ProjectSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    age = serializers.IntegerField()
    city = serializers.CharField(max_length=100)

    def create(self,validated_data):
        return BioData.objects.create(**validated_data)
    
    def update(self,instance,validated_data):
        instance.name = validated_data.get("name",instance.name)
        instance.age = validated_data.get("age",instance.age)
        instance.city = validated_data.get("city",instance.city)
        instance.save()
        
        return instance

class ProjectmodelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BioData
        fields = ['name','age','city']
    
        