from django.contrib import admin
from .models import BIM
from projects.models import Project

# Register your models here.


class BIMAdmin(admin.ModelAdmin):
    list_display=('id','project','bimRequirement','materialDeadline','materialVendor','framingStartDate','modelAvailable','estimatedModelTime','modelDeadline','reviewComplete','comments')
    
admin.site.register(BIM,BIMAdmin)