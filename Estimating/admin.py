from django.contrib import admin
from .models import Location,Estimating,Estimating_detail,Company
from import_export.admin import ImportExportModelAdmin
from django.db.models import Q
from django import forms

import os
from django.contrib import admin
from .models import Estimating,Proposal,Addendum,Specification,Spec_detail,Qualification,ProposalService,UrlsTable,Role,Dprtmnt,DMS_Dertory,GC_detail,AttachedLogoCompany
from nested_admin import NestedStackedInline, NestedModelAdmin # type: ignore
from .forms import EstimatingDetailAdminForm,EstimatingAdminForm
import base64






class RoleAdmin(admin.ModelAdmin):
    list_display=('id','name')


class DprtmntAdmin(admin.ModelAdmin):
    list_display=('id','dprtmnt_name')



class DMS_DertoryAdmin(admin.ModelAdmin):
    # form = CompanyAdminForm
    list_display=('id', 'first_name','last_name','email','job_title','company','department','direct_number','locaton','mobile_number')
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "first_name","last_name", "job_title","mobile_number","company","department","direct_number","locaton"],
            },
        ),
    ]


# Register your models here
class UrlsAdmin(admin.ModelAdmin):
    list_display=('id','url','territory','web_name','ps')



class CompanyAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'Cmpny_Name','adress',
                    'office_phone_number','fax_number',
                    'license_number','email','is_active')
    
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)  # Save the company instance first

        # Handle file attachments
        files = request.FILES.getlist('attached_files')
        for uploaded_file in files:
            # Read and encode the file's content
            binary_data = base64.b64encode(uploaded_file.read())
            AttachedLogoCompany.objects.create(
                company=obj,
                typ=uploaded_file.content_type,
                binary=binary_data,
            )

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, AttachedLogoCompany) and hasattr(instance, 'binary'):
                # Additional handling for AttachedLogoCompany instances if needed
                pass
        super().save_formset(request, form, formset, change)

class LocationAdmin(admin.ModelAdmin):
    list_display=['id','name','is_active']



class GC_detailInline(NestedStackedInline): 
    model = GC_detail
    extra = 1  # Number of extra empty rows to display

class EstimatingAdmin(NestedModelAdmin):
    inlines = [GC_detailInline]
    form=EstimatingAdminForm
    list_display = ['id', 'important_active','start_date', 'prjct_name','time','timezone',
                    'due_date', 'status','company',
                    'bid_amount', 'location', 'estimator',
                    # 'bidder','bidder_mail','bidder_detail'
                    ]
    # list_filter = ['estimator']  # Use 'username' or another field that exists in the 'User' model

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('estimator')  # Optimize the number of SQL queries
        return queryset
    def display_estimators(self, obj):
        # Collect all estimators and estimator managers related to this object
        estimators = obj.estimator.filter(
            Q(job_title__name='Estimator') | Q(job_title__name='Estimating Manager')| Q(job_title__name='Field Management')| Q(job_title__name='Owner')
        )
        # Join their names (or any other relevant field) in a comma-separated string
        return ', '.join([estimator.__str__() for estimator in estimators])
    display_estimators.short_description = 'Estimators/Managers'


class EstimatingDetailAdmin(admin.ModelAdmin):
    list_display=['id','prnt_id','Estimating','drctry_name','file_type','file_name']

    form = EstimatingDetailAdminForm
    def save_model(self, request, obj, form, change):
        if 'file_field' in form.cleaned_data:
            uploaded_file = form.cleaned_data['file_field']
            obj.file_binary_data = uploaded_file.read()

            uploaded_file_name, uploaded_file_extension = os.path.splitext(uploaded_file.name)
            uploaded_file_type = uploaded_file_extension.lstrip('.')
            
            obj.file_name = uploaded_file_name
            obj.file_type = uploaded_file_type

        super().save_model(request, obj, form, change)





class ProposalServiceInline(admin.TabularInline):
    model = ProposalService
    extra = 1
    fk_name = 'proposal'
    # autocomplete_fields = ['service']  # Enable autocomplete for the service field
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


class QualificationInline(NestedStackedInline):
    model = Qualification
    extra = 1 


class ProposalAdmin(NestedModelAdmin):
    inlines = [AddendumInline, ProposalServiceInline, SpecificationInline,QualificationInline]
    list_display = ['id', 'estimating', 'date', 'architect_name', 'architect_firm','plane_date','is_active']
    search_fields = ['architect_name', 'architect_firm']


    def save_model(self, request, obj, form, change):
        # If creating a new proposal (not change), update other proposals
        if not change:
            Proposal.objects.filter(estimating=obj.estimating).update(is_active=False)
            obj.is_active = True  # Set the new proposal as active
        
        super().save_model(request, obj, form, change)




admin.site.register(Company, CompanyAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Estimating, EstimatingAdmin)
admin.site.register(Proposal, ProposalAdmin)
admin.site.register(Estimating_detail, EstimatingDetailAdmin)
admin.site.register(UrlsTable, UrlsAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Dprtmnt, DprtmntAdmin)
admin.site.register(DMS_Dertory, DMS_DertoryAdmin)


