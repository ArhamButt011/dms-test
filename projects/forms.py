from django import forms
from django.contrib import admin
from .models import (
    Project, Contract, Schedule_of_Value, Insurance, Bond, Submittals,
    ShopDrawing, Safity, Schedule, Sub_Contractors, LaborRate, 
    HDS_system,  Buget, Project_detail
)
from Estimating.models import Spec_detail
from django import forms
from django.utils.translation import ugettext_lazy as _

class SubmittalsInlineForm(forms.ModelForm):
    class Meta:
        model = Submittals
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'project') and hasattr(self.instance.project, 'proposal'):
            self.fields['scop_work_number'].queryset = Spec_detail.objects.filter(sefic__proposal=self.instance.project.proposal)

        else:
            self.fields['scop_work_number'].queryset = Spec_detail.objects.none()

class SubmittalsInline(admin.StackedInline):
    model = Submittals
    form = SubmittalsInlineForm
    extra = 1
    
    
    
    