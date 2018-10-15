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
        while (datetime.datetime.now() + datetime.timedelta(seconds=1)).strftime(
                '%Y-%m-%d %H:%M:%S') == self.get_end_time():
            usa_state = WxInterfaceUtil.state(usa_openid['usa_openid'])
            canada_state = WxInterfaceUtil.state(canada_openid['canada_openid'])
            # 判断公众号的关注状态，当点赞次数用完的时候，显示相关提示信息
            if usa_state == 1 and canada_state == 0:
                vote_count = 2
                if vote_count >= 1:
                    select_choice.student.ticket += 1
                    redis_client.zadd('students', select_choice.student.ticket, student_id)
                    SubscribeMessage.objects.create(union_id=union_id['union_id'], student=student_id)
                    usa_state = WxInterfaceUtil.state(openid)
                    canada_state = WxInterfaceUtil.state(openid)
                    vote_count_day = SubscribeMessage.objects.filter(union_id=union_id['union_id'],
                                                                     create_time__lte=self.get_end_time()).count()
                    if vote_count_day <= 5:
                        if usa_state == 1 and canada_state == 0:
                            vote_count += -1
                        elif usa_state == 0 and canada_state == 1:
                            vote_count += - 2 + 3
                        elif usa_state == 1 and canada_state == 1:
                            vote_count += - 1 + 3
                        elif usa_state == 0 and canada_state == 0:
                            vote_count += -2 - 3
                    else:
                        raise exceptions.ValidationError('您今日的投票次数已经用完，请明天再来')
                else:
                    raise exceptions.ValidationError('您当前的投票次数已经用完')

            elif canada_state == 1 and usa_state == 0:
                vote_count = 3
                if vote_count >= 1:
                    select_choice.student.ticket += 1
                    SubscribeMessage.objects.create(union_id=union_id['union_id'], student=student_id)
                    vote_count += -1
                else:
                    raise exceptions.ValidationError('您的投票次数已经用完，关注北美留学生可继续投票')

            elif usa_state == 1 and canada_state == 1:
                vote_count = 5
                if vote_count >= 1:
                    select_choice.student.ticket += 1
                    SubscribeMessage.objects.create(union_id=union_id['union_id'], student=student_id)
                    vote_count += -1
                else:
                    raise exceptions.ValidationError('您的今日投票次数已经用完，请明日再来')

                '''
                   投票过程中。每一次投票后，都要重新判断两个公众号的状态
                   '''
                '''
                关注一次后，给两次投票机会，如果在关注后，投票一次，取消关注，则不能继续投票，  再出去关注，又得到投票机会，
                此时就要判断关注的公众号有了几次投票记录。而且要每次判断两个公众号的关注状态。假如投票一次后，又出去关注了另外一个公众号，则vote_count
                就要加上相应的次数。如果投票一次后，出去取关，则减去相应的次数。  并且控制每天的投票数最大为5.
                '''
        else:
            vote_count = 0
            raise exceptions.ValidationError('关注公众号才能开始投票哦')


class StudentView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class SubscribeMessageView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin,
                           mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):
    queryset = SubscribeMessage.objects.all()
    serializer_class = SubscribeMessageSerializer
