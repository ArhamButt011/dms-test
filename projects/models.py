from codecs import charmap_build
from email.policy import default
from operator import itemgetter
from random import choice
from unittest.util import _MAX_LENGTH
from django.db import models


from accounts.models import User
from Estimating.models import Estimating, Estimating_detail, Proposal,GC_detail,DMS_Dertory








class Project(models.Model):
    status = models.CharField(choices=[ ('Pre-Construction', 'Pre-Construction'),('Construction Phase', 'Construction Phase'), ('Close out phase', 'Close out phase'), 
                                        ('Complete', 'Complete'),], default='Pre-Construction', max_length=50, null=True, blank=True)
    job_num = models.PositiveIntegerField(
        verbose_name="Add Job #", unique=True, null=True, blank=True)
    proposal=models.ForeignKey(Proposal, verbose_name="Add Proposal", on_delete=models.CASCADE, null=True, blank=True)

    prjct_engnr = models.ForeignKey(DMS_Dertory, verbose_name="Project Engineer", related_name='Project_Engineer', limit_choices_to=models.Q(
        job_title__name='Project Engineer'), on_delete=models.SET_NULL, null=True, blank=True) 
    bim_oprtr = models.ForeignKey(DMS_Dertory, verbose_name="BIM Modeler", related_name='Bim_Operator', limit_choices_to=models.Q(job_title__name='BIM') | models.Q(
        job_title__name='BIM Modeler/Trimble Operator') | models.Q(job_title__name='BIM/Manager PR'), on_delete=models.SET_NULL, null=True, blank=True)
    Forman = models.ForeignKey(DMS_Dertory, verbose_name="FOREMAN/Superintendent", related_name='Forman_as_Forman', limit_choices_to=models.Q(job_title__name='Foreman') | models.Q(
        job_title__name='General Superintendent') | models.Q(job_title__name='So. Cal. General Manager') | models.Q(job_title__name='No. Cal. General Manager'), on_delete=models.SET_NULL, null=True, blank=True)
    
    
    
    prjct_mngr = models.ForeignKey(DMS_Dertory, verbose_name="Project Manager", related_name='Project_Manager', limit_choices_to=models.Q(
        job_title__name='Project Manager') | 
        models.Q(job_title__name='Proconstruction Manager') |
        models.Q(job_title__name='Vice President') |
        models.Q(job_title__name='No. Cal. General Manager'),
          on_delete=models.SET_NULL, null=True, blank=True)

    start_date = models.DateField(
        verbose_name="start Date(YYYY-MM-DD)", null=True, blank=True)
    general_superintendent = models.ForeignKey(DMS_Dertory , verbose_name="Genral_superintendent",
                                               limit_choices_to=models.Q(job_title__name='General Superintendent') |
                                               models.Q(job_title__name='So. Cal. General Manager') |
                                               models.Q(job_title__name='No. Cal. General Manager') |
                                               models.Q(job_title__name='President'), on_delete=models.SET_NULL, null=True, blank=True)

    project_address=models.CharField(verbose_name="Add project address", max_length=5000, null=True, blank=True)
    badging=models.BooleanField(default=False)

    addendumStart=models.CharField(verbose_name="Addendum Start", max_length=50, null=True, blank=True)
    addendumEnd=models.CharField(verbose_name="Addendum End", max_length=50, null=True, blank=True)

    important_active=models.BooleanField(default=False)



    contacts_is_active=models.BooleanField(verbose_name="contacts active",null=True,blank=True,default=False)

    contacts=models.CharField(verbose_name="Contacts", max_length=50,choices=[
        ('On build','On build'),('Pending','Pending'),
        ],default='Pending', null=True, blank=True)
    drywell_is_active=models.BooleanField(verbose_name="drawell active",null=True,blank=True,default=False)

    drywell=models.CharField(verbose_name="Drywell Conttrol Joins", max_length=50,choices=[
        ('Submitted','Submitted'),('Working','Working'),('Approved','Approved'),('Pending','Pending'),
        ],default='Pending', null=True, blank=True)
    finish_is_active=models.BooleanField(verbose_name="finish active",null=True,blank=True,default=False)

    finish=models.CharField(verbose_name="FINISH LEVEL MARKUPS", max_length=50,choices=[
        ('Completed','Completed'),('Working','Working'),('Pending','Pending'),
        ],default='Pending', null=True, blank=True)
    wall_type_is_active=models.BooleanField(verbose_name="wall type active",null=True,blank=True,default=False)

    wall_type=models.CharField(verbose_name="WALL TYPE MAPPING", max_length=50,choices=[
        ('Completed','Completed'),('Working','Working'),('Pending','Pending'),
        ],default='Pending', null=True, blank=True)
    ro_door_is_active=models.BooleanField(verbose_name="ro-door active",null=True,blank=True,default=False)

    ro_door=models.CharField(verbose_name="RO-Door", max_length=50,choices=[
        ('Requested','Requested'),('Pending','Pending'),('Received','Received')
        ],default='Pending', null=True, blank=True)
    ro_window_is_active=models.BooleanField(verbose_name="RO-Window active",null=True,blank=True,default=False)

    
    ro_window=models.CharField(verbose_name="RO-Window", max_length=50,choices=[
        ('Requested','Requested'),('Pending','Pending'),('Received','Received')
        ],default='Pending', null=True, blank=True)
    

    substitution=models.CharField(verbose_name="Substitution", max_length=5000, null=True, blank=True)
    
    gc=models.ForeignKey(GC_detail, verbose_name="Add GC", on_delete=models.CASCADE, null=True, blank=True)
    gc_address=models.CharField(verbose_name="GC Address", max_length=5000, null=True, blank=True)
    
    gc_attn = models.CharField(verbose_name="GC attn", max_length=100,null=True,blank=True)
    attn_email=models.EmailField(verbose_name="Add GC Email", max_length=254, null=True, blank=True)
    attn_phone=models.CharField(verbose_name="GC Phone number", max_length=50, null=True, blank=True)
    
    

    
    
    contracts_is_active=models.BooleanField(verbose_name="Contracts active",null=True,blank=True,default=False)
    scheduleOfValue_is_active=models.BooleanField(verbose_name="Schedule of value active",null=True,blank=True,default=False)
    subContractors_is_active=models.BooleanField(verbose_name="Sub Contractors active",null=True,blank=True,default=False)
    budget_is_active=models.BooleanField(verbose_name="Budget active",null=True,blank=True,default=False)
    insurances_is_active=models.BooleanField(verbose_name="Insurances active",null=True,blank=True,default=False)
    schedule_is_active=models.BooleanField(verbose_name="Schedule active",null=True,blank=True,default=False)
    bonds_is_active=models.BooleanField(verbose_name="Bonds active",null=True,blank=True,default=False)
    hdsSystem_is_active=models.BooleanField(verbose_name="HDS System active",null=True,blank=True,default=False)
    wageRate_is_active=models.BooleanField(verbose_name="Wage Rate active",null=True,blank=True,default=False)


    










    def save(self, *args, **kwargs):
        is_new = not self.pk
        super(Project, self).save(*args, **kwargs)
        if is_new:
            created_directories = {}
            def create_directory(name, parent_name=None):
                parent = created_directories.get(parent_name) if parent_name else None
                directory = Project_detail.objects.create(
                    prjct_id=self,
                    drctry_Name=name,
                    prnt_id=parent
                )
                created_directories[name] = directory
                # if estimating_parent:
                #     estimating_to_project[estimating_parent] = directory

            # Top Level Entries

            # for estimating_detail in Estimating_detail.objects.all():
            #     estimating_parent = estimating_detail.prnt
            #     parent_directory = estimating_to_project.get(estimating_parent) if estimating_parent else None
            #     directory = Project_detail.objects.create(
            #         prjct_id=self,
            #         drctry_Name=estimating_detail.drctry_name,
            #         prnt_id=parent_directory,
            #         file_type=estimating_detail.file_type,
            #         file_name=estimating_detail.file_name,
            #         file_binary_data=estimating_detail.file_binary_data
            #     )
            #     estimating_to_project[estimating_detail] = directory

            for name in ['Accounting','Contract', 'Estimating', 'PM', 'Subcontractors']:
                create_directory(name)

            # Second Level Entries
            for item  in [
                {'name': 'Billing', 'parent': 'Accounting'},
                {'name': 'Supplier Invoices', 'parent': 'Accounting'},
                {'name': 'Certified Payroll', 'parent': 'Accounting'},
                {'name': 'Legal', 'parent': 'Accounting'},
                {'name': 'Insurance', 'parent': 'Accounting'},
                {'name': 'COI', 'parent': 'Accounting'},
                {'name': 'Insurance REQ', 'parent': 'Accounting'},
                
                
                
                
                {'name': 'ADD', 'parent': 'Estimating'},
                {'name': 'BID', 'parent': 'Estimating'},
                {'name': 'Plans', 'parent': 'Estimating'},
                {'name': 'Pre BID RFIs', 'parent': 'Estimating'},
                {'name': 'Quates', 'parent': 'Estimating'},
                {'name': 'Specs', 'parent': 'Estimating'},
                {'name': 'W9', 'parent': 'Estimating'},
                {'name': 'Wage Rates', 'parent': 'Estimating'},
                

                
                # {'name': '001', 'parent': 'Change Orders'},
                # {'name': '002', 'parent': 'Change Orders'},
                # {'name': '003', 'parent': 'Change Orders'},
                # {'name': '004', 'parent': 'Change Orders'},
                # {'name': '005', 'parent': 'Change Orders'},
                # {'name': '006', 'parent': 'Change Orders'},
                # {'name': '007', 'parent': 'Change Orders'},
                # {'name': '008', 'parent': 'Change Orders'},
                # {'name': '009', 'parent': 'Change Orders'},
                # {'name': '010', 'parent': 'Change Orders'},
                {'name': 'Contract', 'parent': 'Contract'},
                {'name': 'Contract Documents', 'parent': 'Contract'},
                {'name': 'LOI', 'parent': 'Contract'},
                {'name': 'Bond', 'parent': 'Contract'},
                

                {'name': 'BIM', 'parent': 'PM'},
                {'name': 'Budget Report', 'parent': 'PM'},
                {'name': 'Contacts', 'parent': 'PM'},
                {'name': 'Coordination Meetings', 'parent': 'PM'},
                {'name': 'Delay Notices', 'parent': 'PM'},
                {'name': 'Extra Work', 'parent': 'PM'},
                {'name': 'Inspections', 'parent': 'PM'},
                {'name': 'Material', 'parent': 'PM'},
                {'name': 'Photos', 'parent': 'PM'},
                {'name': 'Plans', 'parent': 'PM'},
                {'name': 'Prelims', 'parent': 'PM'},
                {'name': 'RFIs ASIs', 'parent': 'PM'},
                {'name': 'Schedule', 'parent': 'PM'},
                {'name': 'Specs', 'parent': 'PM'},
                {'name': 'Submittals', 'parent': 'PM'},
                {'name': 'Change Order', 'parent': 'PM'},
                {'name': 'Safety', 'parent': 'PM'},
                
                
                # {'name': 'Emails', 'parent': 'PM'},
                
                
                
                
                # {'name': 'Approved AHAs', 'parent': 'Safety'},
                # {'name': 'Charlies - AHA & Site Specific Safety Plan', 'parent': 'Safety'},

                # {'name': 'Subcontractor Name', 'parent': 'Subcontractors'},
            ]:
                create_directory(item['name'], item['parent'])

            # Third Level Entries
            for item  in [

                
                {'name': 'Delay log', 'parent': 'Delay Notices'},
                
                
                # {'name': 'DIR', 'parent': 'Certified Payroll'},
                # {'name': 'DIR', 'parent': 'Certified Payroll'},
                
                
                # {'name': '2022', 'parent': 'Billing'},
                # {'name': '2023', 'parent': 'Billing'},
                # {'name': 'Billing Form', 'parent': 'Billing'},
                # {'name': 'Releases', 'parent': 'Billing'},
                
                # {'name': 'OLD', 'parent': 'Contract'},
                # {'name': 'Prelim', 'parent': 'Contract Documents'},
                # {'name': 'Abadael Perez', 'parent': 'Badging'},
                # {'name': 'Carmelo Ayala', 'parent': 'Badging'},
                # {'name': 'David Schmitt', 'parent': 'Badging'},
                # {'name': 'Ernesto Rincon', 'parent': 'Badging'},
                # {'name': 'Gonzalo Currasco', 'parent': 'Badging'},
                # {'name': 'Jon Taylor', 'parent': 'Badging'},
                # {'name': 'Juan Currasco', 'parent': 'Badging'},
                # {'name': 'Tylor Tudor', 'parent': 'Badging'},
                # {'name': 'Extra Work Rates', 'parent': 'Extra Work'},
                {'name': 'PCO Log', 'parent': 'Extra Work'},
                # {'name': '00. POs w OAs', 'parent': 'Material'},
                # {'name': '06. Equipment Quotes', 'parent': 'Material'},
                # {'name': 'OAs - Still need a PO', 'parent': 'Material'},
                # {'name': 'Issued For Construction', 'parent': 'Plans'},
                # {'name': 'old', 'parent': 'Plans'},
                # {'name': 'ROUGH OPENINGS', 'parent': 'Plans'},
                # {'name': '100% Plans', 'parent': 'Plans'},
                {'name': 'RFIs/ASI Log', 'parent': 'RFIs ASIs'},
                # {'name': 'Talha Schedules', 'parent': 'Schedule'},
                {'name': 'Submittal Log', 'parent': 'Submittals'},
                {'name': 'Safety Doc Log', 'parent': 'Safety'},

                # {'name': 'Approved', 'parent': 'Submittals'},
                # {'name': 'Badging', 'parent': 'Submittals'},
                # {'name': 'Close Out Docs', 'parent': 'Submittals'},
                # {'name': 'Returned Submittals', 'parent': 'Submittals'},
                # {'name': 'Shop Drawings', 'parent': 'Submittals'},
                # {'name': 'Submittal Catalog', 'parent': 'Submittals'},
                # {'name': 'Title Page & TOC for Submittals', 'parent': 'Submittals'},
                # {'name': 'Working File', 'parent': 'Submittals'},
                # {'name': 'Working File', 'parent': 'Submittals'},
                # {'name': 'Accounting', 'parent': 'Subcontractor Name'},
                # {'name': 'Change Order', 'parent': 'Subcontractor Name'},
                # {'name': 'Contract', 'parent': 'Subcontractor Name'},
                # {'name': 'PM', 'parent': 'Subcontractor Name'},

            ]:
                create_directory(item['name'], item['parent'])
                

            # Fourth Level Entries
            for item  in [
                {'name': 'Delay Notice Template', 'parent': 'Delay log'},
                {'name': 'PCO Template', 'parent': 'PCO Log'},
                {'name': 'RFI Template', 'parent': 'RFIs/ASI Log'},
                {'name': 'Submittal tittal sheet', 'parent': 'Submittal Log'},
                
                
                
                
                
                
                
                
                # {'name': '2023 Wage Rates for Dist', 'parent': 'Extra Work Rates'},
                # {'name': 'PCO 000 - DESCRIPTION', 'parent': 'PCOs'},
                # {'name': 'PCO 001 - Exterior Mock Up - Need to Send', 'parent': 'PCOs'},
                # {'name': 'PCO 002 - IFC Drawing Updates', 'parent': 'PCOs'},
                # {'name': 'PCO 003 - T&M for Mock Up', 'parent': 'PCOs'},
                # {'name': 'Misc pages', 'parent': '100% Plans'},
                # {'name': 'Sent to James .26.23', 'parent': 'Talha Schedules'},
                # {'name': 'Approved', 'parent': 'Returned Submittals'},
                # {'name': 'Exterior', 'parent': 'Shop Drawings'},
                # {'name': 'Interior', 'parent': 'Shop Drawings'},
                # {'name': 'Quotes', 'parent': 'Shop Drawings'},
                # {'name': '01. Product Data', 'parent': 'Submittal Catalog'},
                # {'name': '02. LEED', 'parent': 'Submittal Catalog'},
                # {'name': '03. Product Test Reports', 'parent': 'Submittal Catalog'},
                # {'name': '04. Certificates', 'parent': 'Submittal Catalog'},
                # {'name': '05. Typ Shop Drawings', 'parent': 'Submittal Catalog'},
                # {'name': '06. Trimble Concrete Guide', 'parent': 'Submittal Catalog'},
                # {'name': '05 40 00 - Cold Formed Metal Framing', 'parent': 'Working File'},
                # {'name': '07 21 16 - Mineral Fiber Blanket Insulation', 'parent': 'Working File'},
                # {'name': '07 84 00 - Firestopping', 'parent': 'Working File'},
                # {'name': '07 92 00 - Joint Sealants', 'parent': 'Working File'},

                # {'name': '09 22 00 - Supports for Gyp', 'parent': 'Working File'},
                # {'name': '09 29 00 - Gypsum Board', 'parent': 'Working File'},
                # {'name': 'SEND', 'parent': 'Working File'},
                # {'name': 'Welding Procedures', 'parent': 'Working File'},

            ]:
                # create_directory(item['name'], item['parent'])
                create_directory(itemgetter('name')(item), itemgetter('parent')(item))

            # for item  in [
            #     {'name': 'old', 'parent': 'Exterior'},
            #     {'name': '1. Dewalt', 'parent': '01. Product Data'},
            #     {'name': '3. Ramset', 'parent': '01. Product Data'},
            #     {'name': '4. Simpson', 'parent': '01. Product Data'},
            #     {'name': '05 40 00 - Cold Form Metal Framing', 'parent': '01. Product Data'},
            #     {'name': '07 92 00 - Joint Sealants', 'parent': '01. Product Data'},
            #     {'name': '0924 Lath & Plaster', 'parent': '01. Product Data'},
            #     {'name': '0929 Gypsum Board', 'parent': '01. Product Data'},
            #     {'name': '078440 - Firestopping', 'parent': '01. Product Data'},
            #     {'name': 'Interior', 'parent': '01. Product Data'},
            #     {'name': '092216 - Non-Structural Metal Framing', 'parent': '01. Product Data'},
            #     {'name': 'Backer Rod', 'parent': '01. Product Data'},
            #     {'name': 'Insulation', 'parent': '01. Product Data'},
            #     {'name': 'Insulation', 'parent': '01. Product Data'},
            #     {'name': 'Neoprene Gasket Tape - -Base of wall', 'parent': '01. Product Data'},
            #     {'name': 'RF Shielding - rFoil - with accessories', 'parent': '01. Product Data'},
            #     {'name': 'VOC Certs', 'parent': '02. LEED'},

            #     {'name': '08 Sound Board', 'parent': '09 29 00 - Gypsum Board'},
            #     {'name': 'Mock Up', 'parent': 'SEND'},
            #     {'name': 'Welding Procedures', 'parent': 'SEND'},

            # ]:
            #     create_directory(item['name'], item['parent'])

            # for item  in [

            #     {'name': 'BlazeFrame Product Data', 'parent': '05 40 00 - Cold Form Metal Framing'},
            #     {'name': 'Grabber screws', 'parent': '05 40 00 - Cold Form Metal Framing'},
            #     {'name': 'Header Cripple Stud Clips', 'parent': '05 40 00 - Cold Form Metal Framing'},
            #     {'name': 'Lath', 'parent': '0924 Lath & Plaster'},
            #     {'name': 'Abuse Resistant', 'parent': '0929 Gypsum Board'},
            #     {'name': 'Asbestos Free Certifications', 'parent': '0929 Gypsum Board'},
            #     {'name': 'Cementious Board', 'parent': '0929 Gypsum Board'},
            #     {'name': 'Ext. Gyp Sheathing', 'parent': '0929 Gypsum Board'},
            #     {'name': 'Grabber Screws', 'parent': '0929 Gypsum Board'},
            #     {'name': 'Hilti Screws', 'parent': '0929 Gypsum Board'},
            #     {'name': 'Impact Resistant', 'parent': '0929 Gypsum Board'},
            #     {'name': 'Pre-Rock Drywall', 'parent': '0929 Gypsum Board'},
            #     {'name': 'Shaftwall Liner', 'parent': '0929 Gypsum Board'},
            #     {'name': 'Type X Board', 'parent': '0929 Gypsum Board'},
            #     {'name': 'Water Resistant', 'parent': '0929 Gypsum Board'},
            #     {'name': 'Estimating Tables for Materials', 'parent': '078440 - Firestopping'},
            #     {'name': 'Grabber Firestopping', 'parent': '078440 - Firestopping'},
            #     {'name': 'STI Firestopping', 'parent': '078440 - Firestopping'},
            #     {'name': 'Grabber Screws', 'parent': '092216 - Non-Structural Metal Framing'},
            #     {'name': 'Header Cripple Stud Clips', 'parent': '092216 - Non-Structural Metal Framing'},
            #     {'name': 'Submittal to be updated', 'parent': 'Welding Procedures'},

            # ]:
            #     create_directory(item['name'], item['parent'])

            # for name in [

            #     {'name': 'Amico', 'parent': 'Lath'},
            #     {'name': 'Structa Wire', 'parent': 'Lath'},

            # ]:
            #     create_directory(itemgetter('name')(item), itemgetter('parent')(item)) # type: ignore # type: ignore

    def __str__(self):
        return str(self.proposal)






# class GC_aen(models.Model):
    
#     prjct=models.ForeignKey(Project, verbose_name="Add Project", on_delete=models.CASCADE,null=True,blank=True)

    
    



class Contract(models.Model):
    is_active=models.BooleanField(verbose_name="Important",null=True,blank=True,default=False)
    project=models.ForeignKey(Project, verbose_name="add project", on_delete=models.CASCADE,null=True,blank=True)
    contract=models.CharField(verbose_name="Contract", max_length=50,choices=[
        ('Fully Executed','Fully Executed'),('Pending','Pending')
        ],default='Pending', null=True, blank=True)
    contract_date=models.DateField(verbose_name="add date of the Contract if Fully Executed (YYYY-MM-DD)", null=True, blank=True)


class Schedule_of_Value(models.Model):
    is_active=models.BooleanField(verbose_name="Important",null=True,blank=True,default=False)

    project=models.ForeignKey(Project, verbose_name="add project", on_delete=models.CASCADE,null=True,blank=True)
    schedule=models.CharField(verbose_name="Schedule of Value", max_length=50,choices=[
        ('Approved','Approved'),('Pending','Pending')
        ],default='Pending', null=True, blank=True)
    schedule_date=models.DateField(verbose_name="add date of the schedule if Approved (YYYY-MM-DD)", null=True, blank=True)



class Insurance(models.Model):
    is_active=models.BooleanField(verbose_name="Important",null=True,blank=True,default=False)

    project=models.ForeignKey(Project, verbose_name="add project", on_delete=models.CASCADE,null=True,blank=True)
    insurance=models.CharField(verbose_name="Insurance", max_length=50,choices=[
        ('CCIP','CCIP'),('Sent','Sent'),('Received','Received'),('Completed','Completed'),('Pending','Pending')
        ],default='Pending', null=True, blank=True)
    date=models.DateField(verbose_name="add date(YYYY-MM-DD)", null=True, blank=True)
class Bond(models.Model):
    is_active=models.BooleanField(verbose_name="Important",null=True,blank=True,default=False)

    project=models.ForeignKey(Project, verbose_name="add project", on_delete=models.CASCADE,null=True,blank=True)
    bond=models.CharField(verbose_name="Bond", max_length=50,choices=[
        ('Sent','Sent'),('Received','Received'),('Completed','Completed'),('N/A','N/A'),('Pending','Pending')
        ],default='Pending', null=True, blank=True)
    date=models.DateField(verbose_name="add date(YYYY-MM-DD)", null=True, blank=True)

class Submittals(models.Model):
    is_active=models.BooleanField(verbose_name="Important",null=True,blank=True,default=False)

    project=models.ForeignKey(Project, verbose_name="add project", on_delete=models.CASCADE,null=True,blank=True)
    # scop_work_number=models.ForeignKey(Spec_detail,related_name='scop_work_number', verbose_name="Add scope of Work", on_delete=models.CASCADE, null=True, blank=True)
    dscrptn=models.CharField(verbose_name="Add Description", max_length=5000,null=True,blank=True)
    gc_dcsn=models.CharField(verbose_name="GC Decision", max_length=500, choices=[('Accepted By GC','Accepted By GC'),('Rejected By GC','Rejected By GC')],default='Rejected By GC',null=True,blank=True)
    scopWorkNumber=models.CharField(verbose_name="Add the scop of work Number", max_length=250, null=True, blank=True)
    status=models.CharField(verbose_name="Submittals", max_length=50,choices=[
        ('Approved','Approved'),('Working','Working'),('Submitted','Submitted'),('R & R','R & R'),('Pending','Pending')
        ],default="Pending", null=True, blank=True)
    due_date=models.DateField(verbose_name="add date(YYYY-MM-DD)", null=True, blank=True)
    actn_date=models.DateField(verbose_name="add date(YYYY-MM-DD)", null=True, blank=True)
    LastUpdated_Date=models.DateField(verbose_name="add LastUpdated_Date(YYYY-MM-DD)", null=True, blank=True)


class ShopDrawing(models.Model):
    is_active=models.BooleanField(verbose_name="Important",null=True,blank=True,default=False)

    project=models.ForeignKey(Project, verbose_name="add project", on_delete=models.CASCADE,null=True,blank=True)
    # scop_work_number=models.ForeignKey(Spec_detail,related_name='scop_work_number_shpdrg', verbose_name="Add scope of Work", on_delete=models.CASCADE, null=True, blank=True)
    status=models.CharField(verbose_name="Shop Drawing", max_length=50,choices=[
        ('Approved','Approved'),('Pending','Pending'),
        ],default='Pending', null=True, blank=True)
    date=models.DateField(verbose_name="add date(YYYY-MM-DD)", null=True, blank=True)
    scopWorkNumber=models.CharField(verbose_name="Add the scop of work Number", max_length=250, null=True, blank=True)

class Safity(models.Model):
    is_active=models.BooleanField(verbose_name="Important",null=True,blank=True,default=False)

    project=models.ForeignKey(Project, verbose_name="add project", on_delete=models.CASCADE,null=True,blank=True)
    # scop_work_number=models.ForeignKey(Spec_detail,related_name='scop_work_number_sfty', verbose_name="Add scope of Work", on_delete=models.CASCADE, null=True, blank=True)
    status=models.CharField(verbose_name="Safity", max_length=50,choices=[
        ('Approved','Approved'),('Pending','Pending'),
        ],default='Pending', null=True, blank=True)
    date=models.DateField(verbose_name="add date(YYYY-MM-DD)", null=True, blank=True)
    comment_box=models.CharField(verbose_name="comment", max_length=5000, null=True, blank=True)
    scopWorkNumber=models.CharField(verbose_name="Add the scop of work Number", max_length=250, null=True, blank=True)

class Schedule(models.Model):
    is_active=models.BooleanField(verbose_name="Important",null=True,blank=True,default=False)

    project=models.ForeignKey(Project, verbose_name="add project", on_delete=models.CASCADE,null=True,blank=True)
    status=models.CharField(verbose_name="Schedule", max_length=50,choices=[
        ('Available','Available'),('Requested','Requested'),('Pending','Pending')
        ],default='Pending', null=True, blank=True)
    date=models.DateField(verbose_name="add date(YYYY-MM-DD)", null=True, blank=True)

class Sub_Contractors(models.Model):
    is_active=models.BooleanField(verbose_name="Important",null=True,blank=True,default=False)

    project=models.ForeignKey(Project, verbose_name="add project", on_delete=models.CASCADE,null=True,blank=True)
    status=models.CharField(verbose_name="Sub Contractors", max_length=5000, null=True, blank=True)
    custom=models.CharField(verbose_name="If Custom", max_length=5000, null=True, blank=True)
    name=models.CharField(verbose_name="Sub Contractors Name", max_length=50, null=True, blank=True)
    email=models.EmailField(verbose_name="Email", max_length=254,null=True,blank=True)
    phone=models.CharField(verbose_name="Phone Number", max_length=50,null=True,blank=True)
    date=models.DateField(verbose_name="add date(YYYY-MM-DD)", null=True, blank=True)
    comment_box=models.CharField(verbose_name="comment", max_length=5000, null=True, blank=True)

class LaborRate(models.Model):
    is_active=models.BooleanField(verbose_name="Important",null=True,blank=True,default=False)

    project=models.ForeignKey(Project, verbose_name="add project", on_delete=models.CASCADE,null=True,blank=True)
    status=models.CharField(verbose_name="Labor Rate", max_length=500, null=True, blank=True)
    custom=models.CharField(verbose_name="If Custom", max_length=5000, null=True, blank=True)

    date=models.DateField(verbose_name="add date(YYYY-MM-DD)", null=True, blank=True)
    comment_box=models.CharField(verbose_name="comment", max_length=5000, null=True, blank=True)


class HDS_system(models.Model):
    is_active=models.BooleanField(verbose_name="Important",null=True,blank=True,default=False)

    project=models.ForeignKey(Project, verbose_name="add project", on_delete=models.CASCADE,null=True,blank=True)
    status=models.CharField(verbose_name="HDS System", max_length=500, null=True, blank=True)
    custom=models.CharField(verbose_name="If Custom", max_length=500, null=True, blank=True)

    date=models.DateField(verbose_name="add date(YYYY-MM-DD)", null=True, blank=True)
    comment_box=models.CharField(verbose_name="comment", max_length=5000, null=True, blank=True)


class Buget(models.Model):
    is_active=models.BooleanField(verbose_name="Important",null=True,blank=True,default=False)

    project=models.ForeignKey(Project, verbose_name="add project", on_delete=models.CASCADE,null=True,blank=True)
    status=models.CharField(verbose_name="Labor Rate", max_length=50,choices=[
        ('Pending','Pending'),('Save','Save'),
        ],default='Pending', null=True, blank=True)
    comment_box=models.CharField(verbose_name="comment", max_length=5000, null=True, blank=True)







class WageRate(models.Model):
    project=models.ForeignKey(Project, verbose_name="add project", on_delete=models.CASCADE,null=True,blank=True)
    title_name=models.CharField(verbose_name="Area name", max_length=500,null=True,blank=True)
    st_amount=models.FloatField(verbose_name="ST Amount",blank=True,null=True)
    ot_amount=models.FloatField(verbose_name="OT Amount",blank=True,null=True)
    dt_amount=models.FloatField(verbose_name="DT Amount",blank=True,null=True)





class Project_detail(models.Model):
    drctry_Name = models.CharField(verbose_name="Folder Name", max_length=255)

    prjct_id = models.ForeignKey(
        Project, verbose_name="Project", on_delete=models.CASCADE)
    prnt_id = models.ForeignKey('self', verbose_name="Folder Parent ID",
                                null=True, blank=True, on_delete=models.CASCADE, related_name="children")
    file_type = models.CharField(
        verbose_name="Type Name", max_length=100, null=True, blank=False)
    file_name = models.CharField(
        verbose_name="file Name", max_length=100, null=True, blank=False)
    file_binary_data = models.BinaryField(null=True, blank=True)

    def __str__(self):
        return self.drctry_Name
    
    



class RFI(models.Model):
    project=models.ForeignKey(Project, verbose_name="Select", on_delete=models.CASCADE,null=True,blank=True)
    rfi_num=models.CharField(verbose_name="RFI #",max_length=50,null=True,blank=True)
    date=models.DateField(verbose_name="Date", auto_now=False, auto_now_add=False,null=True,blank=True)
    drwng_rfrnc=models.CharField(verbose_name="Drawing Reference", max_length=500,null=True,blank=True)
    # detl_num=models.IntegerField(verbose_name="Detail No",null=True,blank=True)
    
    detl_num=models.CharField(verbose_name="Detail No", max_length=5000,null=True,blank=True)

    spc_rfrnc=models.CharField(verbose_name="Spec Reference", max_length=500,null=True,blank=True)
    rspns_rqrd=models.DateField(verbose_name="Date", auto_now=False, auto_now_add=False,null=True,blank=True)
    qustn=models.CharField(verbose_name="Question", max_length=5000,null=True,blank=True)
    bool1=models.BooleanField(verbose_name="Other Trades",null=True,blank=True)
    bool2=models.BooleanField(verbose_name="bool2",null=True,blank=True)
    bool3=models.BooleanField(verbose_name="boll3",null=True,blank=True)
    rply_by=models.DateField(verbose_name="Date", auto_now=False, auto_now_add=False,null=True,blank=True)
    rspns=models.CharField(verbose_name="Response",max_length=5000,null=True,blank=True)
    name_log=models.CharField(verbose_name="Name Login", max_length=50,null=True,blank=True)
    title=models.CharField(verbose_name="Title login", max_length=250,null=True,blank=True)
    date2=models.DateField(verbose_name="Date", auto_now=False, auto_now_add=False,null=True,blank=True)
    dscrptn=models.CharField(verbose_name="Description", max_length=5000,null=True,blank=True)


class Attached_Pdf_Rfi(models.Model):
    rfi=models.ForeignKey(RFI, verbose_name="Select RFI", on_delete=models.CASCADE,null=True,blank=True)
    typ=models.CharField(verbose_name="Type of Attachment", max_length=250,null=True,blank=True)
    binary=models.BinaryField("Atthd_pdf", null=True, blank=True, editable=True)
    file_name = models.CharField(verbose_name="File Name", max_length=255, null=True, blank=True)  # New field for file name


class RFI_Log(models.Model):
    project=models.ForeignKey(Project, verbose_name="Select", on_delete=models.CASCADE,null=True,blank=True)
    rfi=models.ForeignKey(RFI, verbose_name="Select RFI", on_delete=models.CASCADE,null=True,blank=True)
    gc_rfi_num=models.CharField(verbose_name="GC RFI#",null=True,blank=True,max_length=50)
    date_close=models.DateField(verbose_name="Date close", auto_now=False, auto_now_add=False,null=True,blank=True)
    status=models.CharField(verbose_name="Status", max_length=50,choices=[
        ('Open','Open'),('Close','Close'),('Void','Void')
        ],default='Open',null=True,blank=True)
    
    cost_schdl=models.CharField(verbose_name="Cost or Schedule", max_length=50,choices=[
        ('Cost','Cost'),('Schedule','Schedule'),('Cost & Schedule','Cost & Schedule'),('None','None')
        ],default='None',null=True,blank=True)
    received_date=models.DateField(verbose_name="Received Date", auto_now=False, auto_now_add=False,null=True,blank=True)

class Attached_Pdf_Rfi_log(models.Model):
    rfi_log=models.ForeignKey(RFI_Log, verbose_name="Select RFI_Log", on_delete=models.CASCADE,null=True,blank=True)
    typ=models.CharField(verbose_name="Type of Attachment", max_length=250,null=True,blank=True)
    binary=models.BinaryField("Atthd_pdf", null=True, blank=True, editable=True)
    file_name = models.CharField(verbose_name="File Name", max_length=255, null=True, blank=True)  # New field for file name


    



    


class PCO(models.Model):
    project=models.ForeignKey(Project,verbose_name="Project",on_delete=models.CASCADE,null=True,blank=True)
    rfi=models.ForeignKey(RFI_Log,verbose_name="Add RFI",on_delete=models.CASCADE,null=True,blank=True)
    date=models.DateField(verbose_name="Current Date", auto_now=False, auto_now_add=False,null=True,blank=True)

    pco_num=models.CharField(verbose_name="PCO NO.", max_length=500,null=True,blank=True)
    asi_num=models.CharField(verbose_name="ASI NO.", max_length=500,null=True,blank=True)
    pci_num=models.CharField(verbose_name="ACI NO.", max_length=500,null=True,blank=True)
    dcrsbsn=models.CharField(verbose_name="PCO Description", max_length=500,null=True,blank=True)
    chnge_dtals=models.CharField(verbose_name="Change Detail", max_length=5000,null=True,blank=True)
    typ=models.CharField(verbose_name="Type of PCO", max_length=500,null=True,blank=True)
    work_day=models.CharField(verbose_name="Estimating Working day", max_length=50,null=True,blank=True)
    mtrl_sub_totl=models.FloatField(verbose_name="Material Sub total ",null=True,blank=True)
    get_tax=models.FloatField(verbose_name="Material Tax",null=True,blank=True)
    value_tax=models.FloatField(verbose_name="Material Tax",null=True,blank=True)
    mtrl_totl=models.FloatField(verbose_name="Material Total",null=True,blank=True)
    mscllns_totl=models.FloatField(verbose_name="Miscellaneous Total",null=True,blank=True)
    lbr_totl=models.FloatField(verbose_name="Labor Total",null=True,blank=True)
    subtotl_cost=models.FloatField(verbose_name="Subtotal Cost",null=True,blank=True)
    get_ohp_tax=models.FloatField(verbose_name="Enter the OH&P @",null=True,blank=True)
    value_ohp_tax=models.FloatField(verbose_name="value of OH&P @",null=True,blank=True)
    cost_ohp_mtrl_tax=models.FloatField(verbose_name="value of Cost + OH&P + Material tax",null=True,blank=True)
    get_bond=models.FloatField(verbose_name="Bond@",null=True,blank=True)
    value_bond=models.FloatField(verbose_name="Value of Bond",null=True,blank=True)
    totl_rqest=models.FloatField(verbose_name="Total Req",null=True,blank=True)
    prpd_by=models.CharField(verbose_name="Login User name", max_length=500, null=True, blank=True)

    
class Attached_Pdf_Pco(models.Model):
    pco=models.ForeignKey(PCO, verbose_name="Select PCO", on_delete=models.CASCADE,null=True,blank=True)
    binary=models.BinaryField("Atthd_pdf", null=True, blank=True, editable=True)
    typ=models.CharField(verbose_name="Type of Attachment", max_length=250,null=True,blank=True)
    file_name = models.CharField(verbose_name="File Name", max_length=255, null=True, blank=True)  # New field for file name



class Qualification(models.Model):
    pco = models.ForeignKey(PCO, verbose_name="PCO", related_name='qualifications', on_delete=models.CASCADE, null=True, blank=True)
    detail=models.CharField(verbose_name="Add Qualification", max_length=5000,null=True,blank=True)
    def __str__(self):
        return self.detail
    
class Debited_Material(models.Model):
    pco = models.ForeignKey(PCO, verbose_name="Debited Material", related_name='debited_materials', on_delete=models.CASCADE, null=True, blank=True)
    itm_name=models.CharField(verbose_name="Material item name", max_length=500,null=True,blank=True)
    quntty=models.FloatField(verbose_name="Quantity", null=True,blank=True)
    unit=models.CharField(verbose_name="Unit", max_length=500,null=True,blank=True)
    unit_prz=models.FloatField(verbose_name="Unit$",null=True,blank=True)
    totl=models.FloatField(verbose_name="Total",null=True,blank=True)
    
class Credited_Material(models.Model):
    pco = models.ForeignKey(PCO, verbose_name="Credited Material", related_name='credited_materials', on_delete=models.CASCADE, null=True, blank=True)
    itm_name=models.CharField(verbose_name="Material item name", max_length=500,null=True,blank=True)
    quntty=models.FloatField(verbose_name="Quantity", null=True,blank=True)
    unit=models.CharField(verbose_name="Unit", max_length=500,null=True,blank=True)
    unit_prz=models.FloatField(verbose_name="Unit$",null=True,blank=True)
    totl=models.FloatField(verbose_name="Total",null=True,blank=True)


class Miscellaneous(models.Model):
    pco = models.ForeignKey(PCO, verbose_name="Miscellaneous", related_name='miscellaneous', on_delete=models.CASCADE, null=True, blank=True)
    itm_name=models.CharField(verbose_name="Material item name", max_length=500,null=True,blank=True)
    quntty=models.FloatField(verbose_name="Quantity", null=True,blank=True)
    unit=models.CharField(verbose_name="Unit", max_length=500,null=True,blank=True)
    unit_prz=models.FloatField(verbose_name="Unit$",null=True,blank=True)
    totl=models.FloatField(verbose_name="Total",null=True,blank=True)



class Labor(models.Model):
    pco = models.ForeignKey(PCO, verbose_name="Labor", related_name='labor', on_delete=models.CASCADE, null=True, blank=True)
    itm_name=models.CharField(verbose_name="Material item name", max_length=500,null=True,blank=True)
    quntty=models.FloatField(verbose_name="Quantity", null=True,blank=True)
    unit=models.CharField(verbose_name="Unit", max_length=500,null=True,blank=True)
    unit_prz=models.FloatField(verbose_name="Unit$",null=True,blank=True)
    totl=models.FloatField(verbose_name="Total",null=True,blank=True)



class PCO_Log(models.Model):
    pco=models.ForeignKey(PCO,verbose_name="PCO",on_delete=models.CASCADE,null=True,blank=True)
    t_m=models.CharField(verbose_name="T&M", max_length=50,null=True,blank=True)
    cor_amont=models.FloatField(verbose_name="Cor Amount",null=True,blank=True)
    co_amont=models.FloatField(verbose_name="C/O Amount",null=True,blank=True)
    co_num=models.CharField(verbose_name="C/O#", max_length=50,null=True,blank=True)
    auther_name=models.CharField(verbose_name="Author Name", max_length=50,null=True,blank=True)
    note=models.CharField(verbose_name="Note", max_length=5000,null=True, blank=True)


class  Delay_Notice(models.Model):
    project=models.ForeignKey(Project, verbose_name="slect project", on_delete=models.CASCADE , blank=True,null=True)
    delay_num=models.CharField(verbose_name="Delay Number #",blank=True,null=True,max_length=50)
    floor=models.CharField(verbose_name="Floor", max_length=500,null=True,blank=True)
    area=models.CharField(verbose_name="area",max_length=500,null=True,blank=True)
    schdul_num=models.CharField(verbose_name="Schedule ID #",max_length=50,null=True,blank=True)
    date=models.DateField(verbose_name="date", auto_now=False,max_length=50, null=True,blank=True)
    rfi_log=models.ForeignKey(RFI_Log, verbose_name="RFI log", on_delete=models.CASCADE,null=True,blank=True)
    pco_log=models.ForeignKey(PCO_Log,verbose_name="PCO",on_delete=models.CASCADE,null=True,blank=True)
    building= models.CharField(verbose_name="Building",max_length=520,null=True,blank=True)
    room=models.CharField(verbose_name="Room",max_length=520,null=True,blank=True)

    dscrptn_impct=models.CharField(verbose_name="Detailed Description of Impact Trade:", max_length=5000 , blank=True, null=True)
    dscrptn_task=models.CharField(verbose_name="Schedule ID # and description of tasks that follow that will be affected:", max_length=5000 , blank=True, null=True)
    comnt=models.CharField(verbose_name="Additional Comments:", max_length=5000,null=True,blank=True)
    preprd_by=models.CharField(verbose_name="Prepared by:", max_length=500,null=True,blank=True)

class Attached_Pdf_Delay(models.Model):
    delay=models.ForeignKey(Delay_Notice, verbose_name="Select Delay Notice", on_delete=models.CASCADE,null=True,blank=True)
    binary=models.BinaryField("Atthd_pdf", null=True, blank=True, editable=True)
    typ=models.CharField(verbose_name="Type of Attachment", max_length=250,null=True,blank=True)
    file_name = models.CharField(verbose_name="File Name", max_length=255, null=True, blank=True)  # New field for file name


class Delay_Log(models.Model):
    dly_ntc=models.ForeignKey(Delay_Notice, verbose_name="Select Delay Notice", on_delete=models.CASCADE,null=True,blank=True)
    date=models.DateField(verbose_name="date", auto_now=False, auto_now_add=False,null=True,blank=True)
    typ=models.CharField(verbose_name="Select status", max_length=50,choices=[
        ('Related PCO','Related PCO'),('Related RFI','Related RFI'),('Other Trades','Other Trades'),
        ],default='Other Trades', null=True, blank=True)
    status=models.CharField(verbose_name="Select status", max_length=50,choices=[
        ('Open','Open'),('Close','Close'),
        ],default='Open', null=True, blank=True)
    dly_rslov=models.DateField(verbose_name="Delay Resolve date", auto_now=False, auto_now_add=False,null=True,blank=True)
    fnl_impct=models.IntegerField(verbose_name="Final Impact (Working Days)",null=True,blank=True)
    unResolvedDelayDays=models.IntegerField(verbose_name="UnResolved Delay Days",null=True,blank=True)

    
    
    
    
    
class BadgingProject(models.Model):
    project=models.ForeignKey(Project, verbose_name="select project", on_delete=models.CASCADE , blank=True,null=True)
    firstName=models.CharField(verbose_name="First Name", max_length=250,null=True,blank=True)
    lastName=models.CharField(verbose_name="Late Name", max_length=250,null=True,blank=True)
    middle=models.CharField(verbose_name="Midle", max_length=250,null=True,blank=True)
    phone=models.CharField(verbose_name="Phone", max_length=250,null=True,blank=True)
    submittedDate=models.DateField(verbose_name="Submitted date", auto_now=False, auto_now_add=False,null=True,blank=True)
    approvedDate=models.DateField(verbose_name="Approved date", auto_now=False, auto_now_add=False,null=True,blank=True)
    resubmitDate=models.DateField(verbose_name="Resubmit date", auto_now=False, auto_now_add=False,null=True,blank=True)
    renewedDate=models.DateField(verbose_name="Renewed date", auto_now=False, auto_now_add=False,null=True,blank=True)
    status=models.CharField(verbose_name="Status", max_length=250,null=True,blank=True)

    tradeExpertise=models.CharField(verbose_name="Trade Expertise", max_length=5000,null=True,blank=True)
    
    
class AddMoreInstance(models.Model):
    badging=models.ForeignKey(BadgingProject, verbose_name="select Badging", on_delete=models.CASCADE , blank=True,null=True)
    instanceName=models.CharField(verbose_name="New Name", max_length=250,null=True,blank=True)
    instanceValue=models.CharField(verbose_name="Value", max_length=250,null=True,blank=True)
    

class TM(models.Model):
    date=models.DateField(verbose_name="Date", auto_now=False, auto_now_add=False,null=True,blank=True)
    tmNumber=models.CharField(verbose_name="T&M #", max_length=250, null=True,blank=True)
    description=models.CharField(verbose_name="Description", max_length=500,null=True,blank=True)

class LaborTM(models.Model):
    tm=models.ForeignKey(TM,verbose_name="select T&M", on_delete=models.CASCADE, null=True, blank=True)
    creaftMan=models.CharField(verbose_name="Craft Man", max_length=250, null=True, blank=True)
    hours=models.FloatField(verbose_name="Hours",null=True,blank=True)

class Material(models.Model):
    tm=models.ForeignKey(TM,verbose_name="select T&M", on_delete=models.CASCADE, null=True, blank=True)
    itemName=models.CharField(verbose_name="Item Name", max_length=250,null=True,blank=True)
    quantity=models.IntegerField(verbose_name="Quantity",null=True,blank=True)
    
class MiscellaneousTM(models.Model):
    tm=models.ForeignKey(TM,verbose_name="select T&M", on_delete=models.CASCADE, null=True, blank=True)
    itemName=models.CharField(verbose_name="Item Name", max_length=250,null=True,blank=True)
    quantity=models.IntegerField(verbose_name="Quantity",null=True,blank=True)

class Attached_Pdf_TM(models.Model):
    tm=models.ForeignKey(TM, verbose_name="Select T&M", on_delete=models.CASCADE,null=True,blank=True)
    binary=models.BinaryField("Atthd_pdf", null=True, blank=True, editable=True)
    typ=models.CharField(verbose_name="Type of Attachment", max_length=250,null=True,blank=True)
    file_name = models.CharField(verbose_name="File Name", max_length=255, null=True, blank=True)  # New field for file name
