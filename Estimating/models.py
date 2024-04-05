from email.policy import default
from django.db import models
from .validation import validate_file_extension
from django.core.exceptions import ValidationError
import os
from django.utils import timezone
# from pytz import timezone as pytz_timezone



# Create your models here.
class Company(models.Model):
    Cmpny_Name = models.CharField(verbose_name="Company Name",max_length=50, null=True, blank=True,unique=True)
    adress=models.CharField(verbose_name="Address",max_length=70, null=True, blank=True)
    office_phone_number = models.CharField(max_length=10, null=True, blank=True)
    fax_number = models.CharField(max_length=10, null=True, blank=True)
    license_number = models.CharField(max_length=50, null=True, blank=True)
    logo = models.ImageField(upload_to='logos/', validators=[validate_file_extension], null=True, blank=True)
    email = models.EmailField(default="estimating@dmsmgt.com", editable=False)
    is_active=models.BooleanField(default=False)
    def __str__(self):
        return self.Cmpny_Name
    

class AttachedLogoCompany(models.Model):
    company=models.ForeignKey(Company, verbose_name="Select Company", on_delete=models.CASCADE,null=True,blank=True)
    typ=models.CharField(verbose_name="Type of Attachment", max_length=250,null=True,blank=True)
    binary=models.BinaryField("Atthd_pdf", null=True, blank=True, editable=True)


class Role(models.Model):
    name=models.CharField(verbose_name="Role", max_length=50,unique=True)
    description = models.TextField(verbose_name="Add Description", blank=True,null=True)
    def __str__(self):
        return self.name





class Dprtmnt(models.Model):
    dprtmnt_name=models.CharField(verbose_name="Add the department name ", max_length=250)
    def __str__(self):
        return self.dprtmnt_name
    





class Location(models.Model):
    name=models.CharField(verbose_name="Location Name",max_length=50,blank=False,null=False)
    is_active=models.BooleanField(default=True)
    def __str__(self):
        return self.name
    






class UrlsTable(models.Model):
    territory = models.CharField(max_length=50)
    web_name = models.CharField(max_length=50)
    url = models.URLField(max_length=200)
    ps = models.CharField(max_length=50,null=True,blank=True)
    def __str__(self):
        return self.web_name
    







class DMS_Dertory(models.Model):
    first_name=models.CharField(verbose_name="First Name", max_length=255,null=True,blank=True)
    last_name=models.CharField(verbose_name="Last Name", max_length=50,null=True,blank=True)
    email = models.EmailField(verbose_name="Email",max_length=255,unique=True,null=True,blank=True)
    job_title = models.ForeignKey(Role,verbose_name="Role", on_delete=models.CASCADE,null=True,blank=True)
    company = models.ForeignKey(Company, verbose_name="company", blank=True, on_delete=models.CASCADE,null=True)
    department=models.ForeignKey(Dprtmnt, verbose_name="Department ", on_delete=models.CASCADE,null=True,blank=True)
    direct_number=models.IntegerField(verbose_name="Direct",null=True,blank=True)
    locaton=models.CharField(verbose_name="Location", max_length=250,null=True,blank=True)
    mobile_number=models.IntegerField(null=True,blank=True,unique=True)
    def __str__ (self):
        return self.first_name




class Estimating(models.Model):
    time = models.TimeField(verbose_name="Time", null=True, blank=True)
    timezone = models.CharField(
        max_length=3,
        choices= [
        ('MST', 'MST'),
        ('CST', 'CST'),
        ('EST', 'EST'),
        ('PST','PST'),],
        verbose_name="Time zone", null=True, blank=True
    )
    prjct_name=models.CharField(verbose_name="Estimate Project Name", max_length=250,null=True,blank=True)
    due_date=models.DateField(verbose_name="Due Date",null=True,blank=True)
    status=models.CharField(max_length=7,
        choices=[
            ('Working','Working'),
            ('Pending','Pending'),
            ('Won','Won'),
            ('Lost','Lost'),],default='Working',null=True,blank=True)
    
    start_date = models.DateField(verbose_name="start Date",null=True,blank=True)
    
    company = models.ForeignKey(Company, verbose_name="Company",related_name='company_in_estimator',limit_choices_to=models.Q(is_active=True), on_delete=models.CASCADE,blank=True,null=True)
    
    bid_amount=models.FloatField(verbose_name="Bid Amount ",blank=True,null=True)
    # location=models.ForeignKey(Location,verbose_name="Add Area", related_name='estimating_as_Area',limit_choices_to=models.Q(is_active=True), on_delete=models.CASCADE,blank=True,null=True)
    location=models.CharField(verbose_name="Location", max_length=250,default="California",null=True,blank=True)
    important_active=models.BooleanField(default=False)

    estimator = models.ForeignKey(
       DMS_Dertory,
        verbose_name="Estimator", related_name='estimations_as_estimator',
        limit_choices_to=models.Q(job_title__name='Estimator')|
        models.Q(job_title__name='Estimating Manager')| models.Q(job_title__name='Field Management')|models.Q(job_title__name='Owner'),
        on_delete=models.SET_NULL, null=True , blank=True)
    # bidder = models.CharField(verbose_name="Bidder Name",max_length=1500, null=True,blank=True)
    # bidder_detail=models.CharField(verbose_name="Bidder Detail",max_length=5000,null=True,blank=True)
    # bidder_mail=models.EmailField(verbose_name="add the bidder Mail", max_length=254,null=True,blank=True)




    # def save(self, *args, **kwargs):
    #     from accounts.models import User
    #     # Check if this is a new instance (i.e., being created and not updated)
    #     is_new = not self.pk
    #     # First, save the Estimating instance (either create or update)
    #     super(Estimating, self).save(*args, **kwargs)
    #     if is_new:
    #         # Top Level Entries
    #         top_level_names = ['Addendums', 'Bid', 'Plans', 'Pre Bid RFIs', 'Quotes', 'Specs']
    #         top_objects = {}
    #         for name in top_level_names:
    #             detail = Estimating_detail.objects.create(Estimating=self, drctry_name=name)
    #             top_objects[name] = detail
    #         # Second Level Entries
    #         second_level_data = [
    #             {'name': 'Add. 3', 'parent': 'Addendums'},
    #             {'name': 'Bid', 'parent': 'Bid'},
    #             {'name': 'Bidders', 'parent': 'Bid'},
    #             {'name': 'Scope', 'parent': 'Bid'},
    #             {'name': 'Plans', 'parent': 'Plans'},
    #             {'name': 'Takeoff', 'parent': 'Plans'},
    #             {'name': '00 Quote Request Plans-Specs', 'parent': 'Quotes'},
    #             {'name': '00A - MC Request Form', 'parent': 'Quotes'},
    #             {'name': '00B - Price Comparison', 'parent': 'Quotes'},
    #             {'name': 'Material Quotes', 'parent': 'Quotes'},
    #             {'name': 'Plaster', 'parent': 'Quotes'},
    #             {'name': 'Scaffold', 'parent': 'Quotes'},
    #             {'name': 'Biding Specs', 'parent': 'Specs'},
    #             {'name': 'Specs', 'parent': 'Specs'}
    #         ]
    #         second_level_objects = {}
    #         for item in second_level_data:
    #             parent_obj = top_objects[item['parent']]
    #             detail = Estimating_detail.objects.create(Estimating=self, drctry_name=item['name'], prnt_id=parent_obj.id)
    #             second_level_objects[item['name']] = detail
    #         # Third Level Entries
    #         third_level_data = [
    #             {'name': 'Emails Pertaining to Job', 'parent': 'Bid'},
    #             {'name': 'FINAL Proposal', 'parent': 'Bid'},
    #             {'name': 'Reference Docs', 'parent': 'Bid'},
    #             {'name': 'Harris', 'parent': 'Bidders'},
    #             {'name': 'OLD', 'parent': '00B - Price Comparison'},
    #             {'name': 'AGS - LOCKED 04-08-2022', 'parent': 'Material Quotes'},
    #             {'name': 'CWalla', 'parent': 'Material Quotes'},
    #             {'name': 'FBM', 'parent': 'Material Quotes'},
    #             {'name': 'Steeler', 'parent': 'Material Quotes'}
    #         ]
    #         third_level_objects = {}
    #         for item in third_level_data:
    #             parent_obj = second_level_objects[item['parent']]
    #             detail = Estimating_detail.objects.create(Estimating=self, drctry_name=item['name'], prnt_id=parent_obj.id)
    #             third_level_objects[item['name']] = detail
    #         # Fourth Level Entries
    #         fourth_level_data = [
    #             {'name': 'Bid Results', 'parent': 'FINAL Proposal'},
    #             {'name': 'OLD', 'parent': 'AGS - LOCKED 04-08-2022'},
    #             {'name': 'OLD', 'parent': 'CWalla'},
    #             {'name': 'OLD', 'parent': 'FBM'},
    #             {'name': 'OLD', 'parent': 'Steeler'}
    #         ]
    #         for item in fourth_level_data:
    #             parent_obj = third_level_objects[item['parent']]
    #             Estimating_detail.objects.create(Estimating=self, drctry_name=item['name'], prnt_id=parent_obj.id)
                
    def __str__(self):
        return self.prjct_name
        




class GC_detail(models.Model):
    estimating = models.ForeignKey(Estimating, on_delete=models.CASCADE, null=True, blank=True,related_name='gc_details')
    gc_name=models.CharField(verbose_name="GC Name",max_length=1500, null=True,blank=True)
    gc_email=models.EmailField(verbose_name="GC Email", max_length=254,null=True,blank=True)
    gc_detail=models.CharField(verbose_name="GC Detail", max_length=1500, null=True,blank=True)
    gc_number=models.IntegerField(verbose_name="GC Number", null=True,blank=True)
    # def __str__ (self):
    #     return self.gc_name
    # def __str__(self):
    #     print(f"GC_detail __str__ called for object with id {self.id}")
    #     return self.gc_name  # Replace with the appropriate field








class Estimating_detail(models.Model):
    Estimating=models.ForeignKey(Estimating,related_name='estimating_details', verbose_name="Add Estimating", on_delete=models.CASCADE)
    prnt = models.ForeignKey('self', verbose_name="Folder Parent ID", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    drctry_name = models.CharField(verbose_name="Folder Name",max_length=255, null=True, blank=True)
    file_type = models.CharField(verbose_name="Type Name",max_length=100, null=True, blank=True)
    file_name = models.CharField(verbose_name="file Name",max_length=100, null=True, blank=True)
    file_binary_data = models.BinaryField(null=True, blank=True)
    def __str__(self):
        return self.drctry_name or "No directory name"
    






##Create perposel
#Service of Exclusion and Inclusion
# class Service(models.Model):
#     name = models.CharField(max_length=255)
#     def __str__(self):
#         return self.name
# #Proposal Table





class Proposal(models.Model):
    estimating=models.ForeignKey(
        Estimating,
        on_delete=models.CASCADE,blank=True,null=True)
    date = models.DateField(
        verbose_name="Proposel Date(YYYY-MM-DD)",
        blank=False,
        null=True)
    architect_name=models.CharField(
        verbose_name="Architect Name",
        max_length=50)
    architect_firm=models.CharField(
        verbose_name="Architect Firm",
        max_length=50)
    plane_date= models.DateField(
        verbose_name="Plane Date(YYYY-MM-DD)",
        blank=True,
        null=True)
    is_active=models.BooleanField(default=True)
    

    def __str__(self):
        return f"Proposal {self.id} by {self.architect_name}" # type: ignore
    



class ProposalService(models.Model):
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE,related_name='services')
    # service = models.ForeignKey(Service, on_delete=models.CASCADE)
    services=models.CharField(verbose_name="Services", max_length=5000, blank=True, null=True)
    service_type = models.CharField(max_length=2, choices=[('IN', 'Inclusion'), ('EX', 'Exclusion')], default='EX') # NEW_INCLUSION, NEW_EXCLUSION etc

    # def __str__(self):
    #     return f"Service {self.services.name} in Proposal {self.proposal.id}" # type: ignore
    



class Addendum(models.Model):
    proposal=models.ForeignKey(Proposal, on_delete=models.CASCADE,related_name='Addendums',null=True,blank=True)
    date = models.DateField(verbose_name="Addendum Date(YYYY-MM-DD)",blank=False,null=True)
    addendum_Number=models.IntegerField(verbose_name="Addendum Number" ,blank=False,null=True)
    def __str__(self):
        return str(self.addendum_Number)
    




class Specification(models.Model):
    proposal=models.ForeignKey(Proposal, on_delete=models.CASCADE,related_name='spcifc',null=True,blank=True)
    specific_name=models.CharField(verbose_name="Scope of Work Name", max_length=250)
    budget=models.FloatField(verbose_name="Scope of Work Price")
    def __str__(self) -> str:
        return self.specific_name
    




class Spec_detail(models.Model):
    sefic=models.ForeignKey(Specification, verbose_name="Specification", on_delete=models.CASCADE,related_name='sefic',null=True,blank=True)
    number=models.CharField(verbose_name="Add Number",max_length=250)
    name=models.CharField(verbose_name="Name", max_length=250, null=True,blank=True)
    def __str__(self) :
        return self.number
    




class Qualification(models.Model):
    
    proposal=models.ForeignKey(Proposal, on_delete=models.CASCADE,related_name='qualification',null=True,blank=True)
    detail=models.CharField(verbose_name="Add Qualification", max_length=255)
    def __str__(self):
        return self.detail
    



