# serializers.py in the "Estimating" app

from django.forms import BooleanField
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
import base64

from Estimating.models import Company,Estimating, Estimating_detail, Proposal, Addendum, Qualification, Spec_detail, Specification, ProposalService, Location,UrlsTable,DMS_Dertory,Dprtmnt,Role,GC_detail,AttachedLogoCompany

from rest_framework.exceptions import ValidationError

from accounts.models import User

from accounts.serializers import UserRegisterationSerializers


class DprtmentSerializers(serializers.ModelSerializer):
    class Meta:
        model=Dprtmnt
        fields=['id','dprtmnt_name']




class Job_titleSerializers(serializers.ModelSerializer):
    class Meta:
        model=Role
        fields=['id','name','description']







class UrlsSerializers(serializers.ModelSerializer):
    class Meta:
        model=UrlsTable
        fields=['id','url','territory','web_name','ps']

class Attache__LogoSerializer(serializers.ModelSerializer):
    binary = serializers.SerializerMethodField()

    def get_binary(self, obj):
        if obj.binary:
            return base64.b64encode(obj.binary).decode('utf-8')
        return None
    class Meta:
        model=AttachedLogoCompany
        fields='__all__'


class CompanySerializer(serializers.ModelSerializer):
    attached_pdfs = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Company
        fields = ['id','is_active','Cmpny_Name','adress','office_phone_number','fax_number','license_number','logo','email','attached_pdfs']

    def get_attached_pdfs(self, obj):
        attached_pdfs = AttachedLogoCompany.objects.filter(company=obj)
        return Attache__LogoSerializer(attached_pdfs, many=True).data
    
    def create(self, validated_data):
        attached_pdfs = self.context['request'].FILES.getlist('attached_pdfs')
        company = Company.objects.create(**validated_data)
        for uploaded_file in attached_pdfs:
            AttachedLogoCompany.objects.create(
                company=company,
                typ=uploaded_file.content_type,
                binary=base64.b64encode(uploaded_file.read()),
            )
        return company



class DMS_DertorySezializers(serializers.ModelSerializer):
    
    company_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Company.objects.all(), source='company',required=False, allow_null=True)

    company=CompanySerializer(read_only=True)
    class Meta:
        model = DMS_Dertory
        fields = ['id', 'first_name','last_name', 'email', 'job_title', 'company_id','company', 'department', 'direct_number', 'locaton', 'mobile_number']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Handle job_title ManyToMany field
        representation['job_title'] = instance.job_title.name if instance.job_title else None
        
        representation['department'] = instance.department.dprtmnt_name if instance.department else None
        
        # Add full_name field
        full_name = f"{instance.first_name or ''} {instance.last_name or ''}".strip()
        representation['full_name'] = full_name if full_name.strip() else None

        return representation

class RecursiveEstimatingDetailSerializer(serializers.Serializer):
    """Serializer for recursive Estimating_detail children."""
    def to_representation(self, value):
        serializer = EstimatingDetailSerializer(value, context=self.context)
        return serializer.data







class EstimatingDetailSerializer(serializers.ModelSerializer):
    children = RecursiveEstimatingDetailSerializer(many=True,read_only=True)

    class Meta:
        model = Estimating_detail
        fields = ['id', 'Estimating', 'prnt', 'drctry_name', 'file_type', 'file_name', 'children']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['Estimating'] = instance.Estimating.prjct_name if instance.Estimating else None
        return representation

class Time12HourField(serializers.TimeField):
    format = "%I:%M %p"

    def to_representation(self, value):
        return value.strftime(self.format)



    
class GC_infoSerializers(serializers.ModelSerializer):
    class Meta:
        model = GC_detail
        fields = ['id','estimating', 'gc_name', 'gc_email', 'gc_detail','gc_number']
        # extra_kwargs = {'id': {'read_only': True}}




    
class EstimatingSerializer(serializers.ModelSerializer):
    gc_details = GC_infoSerializers(many=True, read_only=True)

    time = Time12HourField(format='%I:%M %p', input_formats=['%I:%M %p'], required=False, allow_null=True) # type: ignore

    due_date = serializers.DateField(
        format='%m-%d-%Y', input_formats=['%m-%d-%Y', 'iso-8601'], required=False, allow_null=True) # type: ignore
 
    start_date = serializers.DateField(
        format='%m-%d-%Y', input_formats=['%m-%d-%Y', 'iso-8601'], required=False, allow_null=True) # type: ignore
    # plane_date = serializers.DateField(
    #     format='%m-%d-%Y', input_formats=['%m-%d-%Y', 'iso-8601'], required=False, allow_null=True)
    company_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Company.objects.all(), source='company',required=False, allow_null=True)

    company=CompanySerializer(read_only=True)


    # estimator = UserRegisterationSerializers(read_only=True)  # Serializer for read operation
    # estimator_id = serializers.PrimaryKeyRelatedField(
    #     write_only=True, 
    #     queryset=User.objects.filter(roles__name='Estimator', is_active=True), 
    #     source='estimator', 
    #     required=False, 
    #     allow_null=True
    # )  # Field for write operation
    estimator = DMS_DertorySezializers(read_only=True)
    estimator_id = serializers.PrimaryKeyRelatedField(
    write_only=True,
    queryset=DMS_Dertory.objects.filter(Q(job_title__name='Estimator') | Q(job_title__name='Estimating Manager')
                                        |Q(job_title__name='Field Management')|Q(job_title__name='Owner')),
    source='estimator',
    required=False,
    allow_null=True
)

    estimator = serializers.SerializerMethodField()

    class Meta:
        model = Estimating
        fields = [
            'id',
            'important_active',
            'prjct_name',
            'due_date',
            'time',
            'timezone',
            'status',
            'start_date',
            'bid_amount',
            'company_id',
            'company',
            'location',
            'estimator_id',
            'estimator',
            # 'bidder',
            # 'bidder_mail',
            # 'bidder_detail',
            
            'gc_details',
    
        ]

    
    def get_estimator(self, obj):
        if obj.estimator:
            # Return a simple dict with the estimator's ID
            return DMS_DertorySezializers(obj.estimator).data
        return None
        


    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # representation['location'] = {'id': instance.location.id, 'name': instance.location.name} if instance.location else None
        # representation['estimator'] = instance.estimator.full_Name if instance.estimator else None
        representation['gc_details'] = GC_infoSerializers(instance.gc_details.all(), many=True).data



        return representation





class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name']




class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = ['id','proposal', 'detail']












class SpecificationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spec_detail
        fields = ['id', 'sefic', 'number', 'name']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Updating representation to include names instead of IDs for foreign keys
        representation['sefic'] = instance.sefic.specific_name if instance.sefic else None

        return representation
    



class SpecificationSerializer(serializers.ModelSerializer):
    sefic = SpecificationDetailSerializer(many=True,read_only=True, required=False)

    class Meta:
        model = Specification
        fields = ['id', 'proposal', 'budget', 'specific_name', 'sefic']

    def update(self, instance, validated_data):
        sefics_data = validated_data.pop('sefic', [])
        instance = super().update(instance, validated_data)

        # Update or create Spec_detail instances
        for sefic_data in sefics_data:
            sefic_id = sefic_data.get('id', None)
            if sefic_id:
                # Update existing Spec_detail instance
                sefic_instance = Spec_detail.objects.filter(id=sefic_id, sefic=instance).first()
                if sefic_instance:
                    SpecificationDetailSerializer().update(sefic_instance, sefic_data)
            else:
                # Create new Spec_detail instance
                Spec_detail.objects.create(sefic=instance, **sefic_data)

        return instance





class AddendumSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format='%m-%d-%Y', input_formats=['%m-%d-%Y', 'iso-8601'], required=False, allow_null=True) # type: ignore

    class Meta:
        model = Addendum
        fields = ['id', 'proposal', 'date', 'addendum_Number']





class ProposalServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProposalService
        fields = ['id','proposal', 'services', 'service_type']
    
    
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)


        return representation




class ProposalSerializer(serializers.ModelSerializer):
    services = ProposalServiceSerializer(many=True, read_only=True, required=False, allow_null=True)
    qualification=QualificationSerializer(many=True, read_only=True, required=False, allow_null=True)
    Addendums=AddendumSerializer(many=True,read_only=True, required=False, allow_null=True)
    spcifc=SpecificationSerializer(many=True,read_only=True, required=False, allow_null=True)
    estimating_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Estimating.objects.all(), source='estimating', required=True)
    date = serializers.DateField(format='%m-%d-%Y', input_formats=['%m-%d-%Y', 'iso-8601'], required=False, allow_null=True) # type: ignore
    plane_date = serializers.DateField(format='%m-%d-%Y', input_formats=['%m-%d-%Y', 'iso-8601'], required=False, allow_null=True) # type: ignore
    estimating=EstimatingSerializer(read_only=True)
    
    
    class Meta:
        model = Proposal
        fields = ['id', 'estimating_id', 'date','architect_name','plane_date','is_active', 'architect_firm','Addendums', 'services','spcifc','estimating','qualification'] 

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)


    #     representation['estimating'] = instance.estimating.prjct_name if instance.estimating else None


    #     return representation
