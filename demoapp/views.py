#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from .models import Backup_mysql

# Create your views here.

 
def index(request):
    return HttpResponse(u"欢迎!")


def backup_detail(request):
    if request.method == 'GET': 
        bkmysql = Backup_mysql.objects.order_by("id")[0:50]
        return render(request, 'bkmysql.html', {'bkmysql': bkmysql})
    elif request.method == 'POST':
        result = request.POST.get('result','fail')
        #task_id = request.POST.get('task_id')
        bkmysql = Backup_mysql.objects.filter(result__startswith=result).order_by("-end_date")[:20]
        return render(request, 'bkmysql.html', {'bkmysql': bkmysql})
