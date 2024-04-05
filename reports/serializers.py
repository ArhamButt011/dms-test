from rest_framework import serializers
from .models import WageRateDetail, WageRate

class WageRateDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WageRateDetail
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation

class WageRateSerializer(serializers.ModelSerializer):
    detail=WageRateDetailSerializer(source='wageratedetail_set',many=True,required=False)

    class Meta:
        model = WageRate
        fields = ['id', 'title','detail']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.required = False
    def save(self,**Kwargs):
        detail_data=self.validated_data.pop('wageratedetail_set',[])#type:ignore
        wage_instance = super().save(**kwargs)#type:ignore
        self._save_nested_data(detail_data, WageRateDetail, wage_instance)
        return wage_instance
    def _save_nested_data(self,data_list,ModelClass,parent_instance):
        for data in data_list:
            ModelClass.objects.create(pco=parent_instance,**data)
            



