from django.db import models
from apps.oaauther.models import OAUser


class AbsentStatusChoices(models.IntegerChoices):
    AUDITING = 1    # 审批中
    PASS = 2        # 通过
    REJECT = 3      # 拒绝


class AbsentType(models.Model):
    name = models.CharField(max_length=100)
    created_time = models.DateTimeField(auto_now_add=True)


class Absent(models.Model):
    # 标题
    title = models.CharField(max_length=100)
    # 请假原因
    reason_text = models.TextField()
    # 请假类型
    absent_type = models.ForeignKey(AbsentType, on_delete=models.CASCADE,related_name='absents',related_query_name='absents')
    # 发起人
    requester = models.ForeignKey(OAUser, on_delete=models.CASCADE,related_name='my_absents',related_query_name='my_absents')
    # 审批人
    responser = models.ForeignKey(OAUser, on_delete=models.CASCADE,related_name='sub_absents',related_query_name='sub_absents',null=True)
    # 状态 默认审批中
    status = models.IntegerField(choices=AbsentStatusChoices,default=AbsentStatusChoices.AUDITING)
    # 开始日期
    start_date = models.DateField()
    # 结束日期
    end_date = models.DateField()
    # 发起时间
    created_time = models.DateTimeField(auto_now_add=True)
    # 回复内容
    response_context = models.TextField(blank=True)
