from django.contrib import admin
from .models import WageRateDetail,WageRate
from nested_admin import NestedStackedInline, NestedModelAdmin # type: ignore

# Register your models here.

class WageRateDetailInline(NestedStackedInline):
    model=WageRateDetail
    extra=1
    
    
    
class WageRateAdmin(admin.ModelAdmin):
    inlines=[WageRateDetailInline]
    list_display=('id','title')


    
admin.site.register(WageRate,WageRateAdmin)
# admin.site.register(WageRateDetail)