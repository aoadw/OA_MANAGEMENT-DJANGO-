from django.db import models
from apps.oaauther.models import OAUser,OADepartment


class Inform(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    public = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    departments = models.ManyToManyField(OADepartment,related_name='informs',related_query_name='informs')
    author = models.ForeignKey(OAUser,on_delete=models.CASCADE,related_name='informs',related_query_name='informs')

    class Meta:
        # 按最新发布时间排序
        ordering = ['-created_time']


class InformRead(models.Model):
    inform = models.ForeignKey(Inform,on_delete=models.CASCADE,related_name='read',related_query_name='read')
    user = models.ForeignKey(OAUser,on_delete=models.CASCADE,related_name='read',related_query_name='read')
    read_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 设置inform和user绑定的数据是唯一的
        unique_together = (('inform','user'),)
