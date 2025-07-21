from django.db import models

class employee_groups(models.Model):
    ifid = models.IntegerField()
    name = models.CharField(max_length=100)
    entity = models.CharField(max_length=100)  # Add this!

    def __str__(self):
        return f"{self.name} ({self.ifid})"