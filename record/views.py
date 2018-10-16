from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets, serializers
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import exceptions
from record.function import WxInterfaceUtil
from utils.redis_server import redis_client
from datetime import datetime
import datetime
import time
from record.models import User, VoteRecord, Student, SubscribeMessage
from record.serializers import UserSerializer, VoteRecordSerializer, StudentSerializer, SubscribeMessageSerializer


class UserView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
               viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class VoteRecordView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = VoteRecord.objects.all()
    serializer_class = VoteRecordSerializer

    #
    # def vote_count(self,usa_state,canada_state):
    # 获取第二天的凌晨0点的时间
    def get_end_time(self):
        tt = datetime.now().timetuple()
        unix_ts = time.mktime(tt)
        result = unix_ts + 86400 - tt.tm_hour * 60 * 60 - tt.tm_min * 60 - tt.tm_sec
        return datetime.fromtimestamp(result)

    @list_route(['POST'])
    def vote(self, request, openid):
        student_id = request.data.get('student_id')
        vote_to = get_object_or_404(Student, pk=student_id)
        usaopenid = SubscribeMessage.objects.filter(usa_openid=openid)
        # 如果usa_openid存在，则表示传入的openid是关注的北美留学生的openid
        if usaopenid.exists():
            union_id = SubscribeMessage.objects.filter(usa_openid=openid).values('union_id')
            usa_openid = SubscribeMessage.objects.filter(usa_openid=openid).values('usa_openid')
            canada_openid = SubscribeMessage.objects.filter(usa_openid=openid).values('canada_openid')
            # usa_state = WxInterfaceUtil.state(usa_openid['usa_openid'])
            # canada_state = WxInterfaceUtil.state(canada_openid['canada_openid'])
        # 否则，传入的openid是关注加拿大问吧的openid
        else:
            union_id = SubscribeMessage.objects.filter(canada_openid=openid).values('union_id')
            usa_openid = SubscribeMessage.objects.filter(canada_openid=openid).values('usa_openid')
            canada_openid = SubscribeMessage.objects.filter(canada_openid=openid).values('canada_openid')
        # 根据student_id获取被投票人对象
        select_choice = vote_to.voterecord_set.get(student_id)
        # 定时凌晨0点刷新
        while (datetime.datetime.now() + datetime.timedelta(seconds=1)).strftime(
                '%Y-%m-%d %H:%M:%S') == self.get_end_time():
            usa_state = WxInterfaceUtil.state(usa_openid['usa_openid'])
            canada_state = WxInterfaceUtil.state(canada_openid['canada_openid'])
            vote_count_day = SubscribeMessage.objects.filter(union_id=union_id['union_id'],
                                                             create_time__lte=self.get_end_time()).count()
            # 判断公众号的关注状态，当点赞次数用完的时候，显示相关提示信息
            if usa_state == 1 and canada_state == 0:
                # 每一次投票都是重新调用vote这个函数，当在这一天没有投票，vote_count_day为0时，此时的投票次数不变为2.
                # 如果vote_count_day为1时，这时，就要在当前状态下的投票次数-1.
                vote_count = 2 - vote_count_day
                # 如果投票次数大于0，并且一天总投票数小于6
                if vote_count >= 1 and vote_count_day <= 5:
                    select_choice.student.ticket += 1
                    redis_client.zadd('students', select_choice.student.ticket, student_id)
                    '''这里还可以求出学生票数的排名，并返回'''
                    SubscribeMessage.objects.create(union_id=union_id['union_id'], student=student_id)
                    return Response(student_id, select_choice.student.ticket, union_id['union_id'])
                    # usa_state = WxInterfaceUtil.state(usa_openid['usa_openid'])
                    # canada_state = WxInterfaceUtil.state(canada_openid['canada_openid'])
                    # if usa_state == 1 and canada_state == 0:
                    #     vote_count += -1
                    # elif usa_state == 0 and canada_state == 1:
                    #     vote_count += - 2 + 3
                    # elif usa_state == 1 and canada_state == 1:
                    #     vote_count += - 1 + 3
                    # # elif usa_state == 0 and canada_state == 0:
                    # #     vote_count += -2 - 3
                    # else:
                    #     raise  exceptions.ValidationError('请先关注再来投票')
                else:
                    raise exceptions.ValidationError('您的投票次数已经用完')
                # else:
                #     raise exceptions.ValidationError('您当前的投票次数已经用完')

            elif usa_state == 0 and canada_state == 1:
                vote_count = 3 - vote_count_day
                if vote_count >= 1 and vote_count_day <= 5:
                    select_choice.student.ticket += 1
                    redis_client.zadd('students', select_choice.student.ticket, student_id)
                    SubscribeMessage.objects.create(union_id=union_id['union_id'], student=student_id)
                    return Response(student_id, select_choice.student.ticket, union_id['union_id'])
                    # usa_state = WxInterfaceUtil.state(usa_openid['usa_openid'])
                    # canada_state = WxInterfaceUtil.state(canada_openid['canada_openid'])
                    # if usa_state==0 and canada_state==1:
                    #     vote_count += -1
                    # elif usa_state==1 and canada_state==0:
                    #     vote_count +=-3+2
                else:
                    raise exceptions.ValidationError('您的投票次数已经用完')

            elif usa_state == 1 and canada_state == 1:
                vote_count = 5 - vote_count_day
                if vote_count >= 1 and vote_count_day <= 5:
                    select_choice.student.ticket += 1
                    redis_client.zadd('students', select_choice.student.ticket, student_id)
                    SubscribeMessage.objects.create(union_id=union_id['union_id'], student=student_id)
                    return Response(student_id, select_choice.student.ticket, union_id['union_id'])

                else:
                    raise exceptions.ValidationError('您的今日投票次数已经用完，请明日再来')

        else:
            vote_count = 0
            raise exceptions.ValidationError('关注公众号才能开始投票哦')

    @list_route()
    def rank(self):
        students_rank = redis_client.zrange('students', 0, -1)
        return Response(students_rank)


class StudentView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class SubscribeMessageView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin,
                           mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):
    queryset = SubscribeMessage.objects.all()
    serializer_class = SubscribeMessageSerializer
