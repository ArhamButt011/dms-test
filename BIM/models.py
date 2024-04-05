from django.db import models
from projects.models import Project
# Create your models here.

class BIM(models.Model):
    project=models.ForeignKey(Project, verbose_name="Select Project", on_delete=models.CASCADE,null=True,blank=True)
    bimRequirement=models.BooleanField(default=True,null=True,blank=True)
    materialDeadline=models.DateField(verbose_name="Material Order Deadline", auto_now=False, auto_now_add=False,null=True,blank=True)
    materialVendor=models.CharField(verbose_name="Material", max_length=50,null=True,blank=True)
    framingStartDate=models.DateField(verbose_name="Metal Framing Scheduled Start Date", auto_now=False, auto_now_add=False,null=True,blank=True)
    modelAvailable=models.BooleanField(verbose_name="Architect Model available",default=True,null=True,blank=True)
    estimatedModelTime=models.IntegerField(verbose_name="Estimated Modeling Time Unit",null=True,blank=True)
    modelDeadline=models.DateField(verbose_name="Model Deadline Metal Framing + Revit", auto_now=False, auto_now_add=False,null=True,blank=True)
    reviewComplete=models.FloatField(verbose_name="% Review complete",null=True,blank=True)
    comments=models.CharField(verbose_name="Comments/Missing Items ", max_length=5000,null=True,blank=True)
