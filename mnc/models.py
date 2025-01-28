from django.db import models
from django.utils import timezone
class Master_Table_Lists(models.Model):
    Table_Name=models.CharField(max_length=200)
    Last_Update=models.CharField(max_length=200)
    Duration=models.CharField(max_length=100)
    New_Update=models.CharField(max_length=100)  

class Example_master(models.Model):
    Table_Name=models.CharField(max_length=40)
    Last_Update=models.DateTimeField(default=timezone.now)
    Duration=models.CharField(max_length=3)
    New_Update=models.CharField(max_length=40)


    
