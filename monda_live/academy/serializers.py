from rest_framework import serializers
from .models import Attendance, CourseGroupMember

class CourseGroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseGroupMember
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        exclude = ['check_out']