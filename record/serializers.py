from rest_framework import serializers

from record.models import User, VoteRecord, Student, SubscribeMessage


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['open_id', 'union_id', 'operation', 'name', 'email', 'phone', 'create_time', 'modified_time']


class VoteRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteRecord
        fields = ['union_id', 'student', 'create_time', 'modified_time']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'major', 'school', 'ticket', 'detail', 'create_time', 'modified_time']


class SubscribeMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscribeMessage
        fields = ['union_id', 'usa_openid', 'canada_openid', 'create_time', 'modified_time']
