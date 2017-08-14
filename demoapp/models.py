from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Backup_mysql(models.Model):
    task_name = models.CharField(max_length=30,blank=True)
    task_id = models.CharField(max_length=50,blank=True)
    start_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True,null=True)
    result = models.CharField(max_length=100,blank=True,null=True)
    task_status = models.CharField(max_length=10,blank=True)
    host_ip = models.CharField(max_length=30,blank=True,null=True)
     
    def __unicode__(self):
        return self.task_id+self.task_name
