from django.contrib import admin
from .models import User,UserRole,Department
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse


# Register your models here.


class UserModelAdmin(BaseUserAdmin):
    def get_roles(self, obj):
        return ", ".join([str(role) for role in obj.roles.all()])
    get_roles.short_description = 'Roles'

    

    # The fields to be used in displaying the User model.
    list_display = [
        "id", "email", "full_Name", "is_admin", "is_active", "get_roles",
        "phone_number", "company", "department", "direct_number", "locaton"
    ]
    list_filter = ["is_admin", "is_active"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {
            "fields": [
                "full_Name", "phone_number", "department",
                "direct_number", "locaton","signtr"
            ]
        }),
        ("Permissions", {
            "fields": ["is_admin", "roles", "is_active", "company"]
        }),
    ]
    # No need for signature_link method or signature field in fieldsets
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email", "full_Name", "password1", "password2", "roles",
                    "phone_number", "is_active", "company", "department",
                    "direct_number", "locaton"
                ],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email", "id"]
    filter_horizontal = ['roles',]

class DepartmentAdmin(admin.ModelAdmin):
    list_display=['id','dprtmnt_name']


class UserRoleAdmin(admin.ModelAdmin):
    list_display=['id','name','description']


# Now register the new UserAdmin...
admin.site.register(User, UserModelAdmin)
admin.site.register(UserRole,UserRoleAdmin)
admin.site.register(Department,DepartmentAdmin)
