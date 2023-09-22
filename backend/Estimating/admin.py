from django.contrib import admin
from .models import Location,Estimating,Estimating_detail
from django.core.files.storage import default_storage

import os
from django.contrib import admin
from .models import Estimating,Proposal,Service,Addendum,Specification,Spec_detail,Qualification,ProposalService
from nested_admin import NestedStackedInline, NestedModelAdmin
from .forms import EstimatingDetailAdminForm


# Register your models here
class LocationAdmin(admin.ModelAdmin):
    list_display=['id','name']






class EstimatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'start_date', 'Prjct_Name', 'due_date', 'status',
                    'company', 'bid_amount', 'location', 'estimator', 'bidder']
    list_filter = ['estimator']  # Use 'username' or another field that exists in the 'User' model

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('estimator')  # Optimize the number of SQL queries
        return queryset







class EstimatingDetailAdmin(admin.ModelAdmin):
    list_display=['id','prnt_id','Estimating','drctry_name','file_type','output_Table_Name']

    form = EstimatingDetailAdminForm
    def save_model(self, request, obj, form, change):
        if 'file_field' in form.cleaned_data:
            uploaded_file = form.cleaned_data['file_field']
            obj.file_binary_data = uploaded_file.read()

            uploaded_file_name, uploaded_file_extension = os.path.splitext(uploaded_file.name)
            uploaded_file_type = uploaded_file_extension.lstrip('.')
            
            obj.output_Table_Name = uploaded_file_name
            obj.file_type = uploaded_file_type

        super().save_model(request, obj, form, change)





class ProposalServiceInline(admin.TabularInline):
    model = ProposalService
    extra = 1
    fk_name = 'proposal'
    autocomplete_fields = ['service']  # Enable autocomplete for the service field
    sortable_options = {}  # Keeping this to avoid the error you mentioned earlier



class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']





class AddendumInline(NestedStackedInline):
    model = Addendum
    extra = 1  # Number of extra empty rows to display
    
class SpecificationDetailInline(NestedStackedInline):
    model = Spec_detail
    extra = 1  # Number of extra empty rows to display



class SpecificationInline(NestedStackedInline): 
    model = Specification
    extra = 1  # Number of extra empty rows to display
    inlines = [SpecificationDetailInline]  # Nested inline for Spec_detail within Specification




class ProposalAdmin(NestedModelAdmin):
    inlines = [AddendumInline, ProposalServiceInline, SpecificationInline]
    list_display = ['id', 'estimating', 'date', 'architect_name', 'architect_firm']
    search_fields = ['architect_name', 'architect_firm']



class QualificationAdmin(admin.ModelAdmin):
    list_display=['id','detail']

admin.site.register(Location,LocationAdmin)
admin.site.register(Estimating, EstimatingAdmin)
admin.site.register(Proposal,ProposalAdmin)
admin.site.register(Service,ServiceAdmin)
admin.site.register(Qualification,QualificationAdmin)
admin.site.register(Estimating_detail,EstimatingDetailAdmin)






# class ProposalsAdmin(admin.ModelAdmin):
       
#     list_display = ['id', 'estimating', 'date', 'architect_name', 'architect_firm']
#     search_fields = ['architect_name', 'architect_firm']
#     list_filter = ['date']


# class ServiceAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'type']
#     search_fields = ['name']
#     list_filter = ['type']





# class ProposalServiceAdmin(admin.ModelAdmin):
#     list_display = ['id', 'proposal', 'service', 'type', 'edited_type']
#     search_fields = ['service__name']
#     list_filter = ['type', 'edited_type']
