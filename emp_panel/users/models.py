from django.db import models

class empinfo(models.Model):
    
    ifid = models.IntegerField(null=True)
    name = models.CharField(max_length=250)
    mobileno = models.IntegerField(null=True)

    class Meta:
        unique_together = ('name', 'ifid') 
