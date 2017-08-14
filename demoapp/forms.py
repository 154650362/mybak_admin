# -*- coding: UTF-8 -*-  
from django.forms import ModelForm  
from .models import Backup_mysql

class Backup_mysqlForm(ModelForm):
    class Meta:
        model = Backup_mysql
        fields = '__all__'

