from django.db import models


class User(models.Model):
    OPTION_CHOICE = (
        (0, '关注加拿大留学生问吧'),
        (1, '关注北美留学生'),
        (2, '全部关注'),
        (3, '没关注'),
        (4, '取关问吧'),
        (5, '取关北美'),
    )
    open_id = models.CharField('open_id', max_length=64)
    union_id = models.CharField('union_id', max_length=64)
    operation = models.IntegerField('操作类型', choices=OPTION_CHOICE)
    name = models.CharField('姓名', max_length=64, null=True)
    email = models.EmailField('邮箱', max_length=30, null=True)
    phone = models.CharField('联系手机', max_length=30, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True, null=True)
    modified_time = models.DateTimeField('修改时间', auto_now=True, null=True)

    class Meta:
        db_table = "user"


class Student(models.Model):
    name = models.CharField('姓名', max_length=64, null=True)
    major = models.CharField('专业', max_length=64, null=True)
    school = models.CharField('院校', max_length=64, null=True)
    ticket = models.IntegerField('票数', null=True)
    detail = models.CharField('自我介绍', max_length=255, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True, null=True)
    modified_time = models.DateTimeField('修改时间', auto_now=True, null=True)

    class Meta:
        db_table = "student"


class SubscribeMessage(models.Model):
    union_id = models.CharField('union_id', max_length=64, null=True)
    usa_openid = models.CharField('北美留学生openid', max_length=64, null=True)
    canada_openid = models.CharField('加拿大问吧openid', max_length=64, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True, null=True)
    modified_time = models.DateTimeField('修改时间', auto_now=True, null=True)

    class Meta:
        db_table = "subscribe_message"


class VoteRecord(models.Model):
    union_id = models.CharField('union_id', max_length=64, primary_key=True)
    student = models.ForeignKey(Student, max_length=30, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True, null=True)
    modified_time = models.DateTimeField('修改时间', auto_now=True, null=True)

    class Meta:
        db_table = "vote_record"
