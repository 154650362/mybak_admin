#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import  
from celery import shared_task
from celery import Task
from celery import Task
try:
    import paramiko
except:
    import paramiko110 as paramiko
try:
    import json
except:
    import simplejson as json
import subprocess
import time
from .models import Backup_mysql



#system parms
username = 'mysql'
password = 'mysql'
port = 3389
remote_mysql_data_path = '/mysql/data'
mysqlrsa='/home/mysql/.ssh/id_rsa'
ssh = 0 #1表示无密码登录，0表示有密码登录


def runCmd(cmd):
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    except:
        return None, p.returncode
    else:
        output, err = p.communicate()
    return output, p.returncode

def sshclient_execmd_ps(hostname,execmd,port=port, username=username, password=password):
    paramiko.util.log_to_file("paramiko.log")
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname=hostname, port=port, username=username, password=password)
    stdin, stdout, stderr = s.exec_command (execmd)
    stdin.write("Y")  # Generally speaking, the first connection, need a simple interaction.
    out = stdout.read()
    print out
    s.close()
    return out

def sshclient_execmd_rsa(hostname,execmd,port=port, username=username, pkey=mysqlrsa):
    paramiko.util.log_to_file("paramiko.log")
    key = paramiko.RSAKey.from_private_key_file(pkey)
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname=hostname, port=port, username=username,pkey=key )
    stdin, stdout, stderr = s.exec_command (execmd)
    stdin.write("Y")  # Generally speaking, the first connection, need a simple interaction.
    out = stdout.read()
    s.close()
    return out

if ssh == 1:
    sshclient_execmd = sshclient_execmd_rsa
elif ssh == 0:
    sshclient_execmd = sshclient_execmd_ps

class MyTask(Task):
    def __init__(self):
        self.start_time=None
        self.end_time=None

    def on_success(self, retval, task_id, args, kwargs):
        self.end_time=time.ctime()
        print self.name,self.start_time,self.end_time,self.request.id
        print('{0!r} success: {1!r},result:{2},'.format(task_id, args,retval))
        print 'task done: {0}'.format(retval)
        return super(MyTask, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))
        print 'task fail, reason: {0}'.format(exc)
        return super(MyTask, self).on_failure(exc, task_id, args, kwargs, einfo)


 
@shared_task  
def add(x, y):  
    return x + y  
 
@shared_task  
def mul(x, y):  
    return x * y  
 
@shared_task  
def xsum(numbers):  
    return sum(numbers)


@shared_task(base=MyTask,bind=True)
def backup(self,hostname):
    self.start_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    myback=Backup_mysql.objects.create(task_name=self.name,task_id=self.request.id,start_date=self.start_time,task_status='starting',host_ip=self.request.args[0])
    myback.save()
    out = sshclient_execmd(hostname,execmd='/usr/bin/python /home/mysql/ran.py')
    self.end_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    myback.end_date=self.end_time
    myback.result=out
    myback.task_status='end'
    myback.save()
    return out,self.name,self.start_time,self.end_time,self.request.id

