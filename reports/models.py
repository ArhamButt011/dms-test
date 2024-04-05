from typing import Any
from django.db import models

# Create your models here.


class WageRate(models.Model):
    title=models.CharField(verbose_name="Add Title", max_length=250,null=True,blank=True)
    
    def __str__(self):
        return self.title

class WageRateDetail(models.Model):
    title=models.ForeignKey(WageRate, verbose_name="Add Title", on_delete=models.CASCADE)
    area_name=models.CharField(verbose_name="Area name", max_length=500,null=True,blank=True)
    st_amount=models.FloatField(verbose_name="ST Amount",blank=True,null=True)
    ot_amount=models.FloatField(verbose_name="OT Amount",blank=True,null=True)
    dt_amount=models.FloatField(verbose_name="DT Amount",blank=True,null=True)
    
    def __str__(self):
        return self.area_name