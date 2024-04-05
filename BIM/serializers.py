from rest_framework import serializers
from .models import BIM
from projects.models import Project
from projects.serializers import ProjectSerializer
import datetime


class BimSerializer(serializers.ModelSerializer):
    materialDeadline = serializers.DateField(
        format='%m-%d-%Y', input_formats=['%m-%d-%Y', 'iso-8601'], required=False, allow_null=True) #type:ignore
    framingStartDate = serializers.DateField(
        format='%m-%d-%Y', input_formats=['%m-%d-%Y', 'iso-8601'], required=False, allow_null=True)#type:ignore
    modelDeadline = serializers.DateField(
        format='%m-%d-%Y', input_formats=['%m-%d-%Y', 'iso-8601'], required=False, allow_null=True)#type:ignore
    
    project_id=serializers.PrimaryKeyRelatedField(write_only=True, queryset=Project.objects.all(), source='project', required=False)
    project=ProjectSerializer(read_only=True)
    
    class Meta:
        model=BIM
        fields=['id','project_id','bimRequirement','materialDeadline','materialVendor','framingStartDate','modelAvailable','estimatedModelTime','modelDeadline','reviewComplete','comments','project']

