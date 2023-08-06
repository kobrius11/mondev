from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import permissions
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .. import models 
from ..serializers import AttendanceSerializer


class CheckIn(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AttendanceSerializer

    def get_course_group(self):
        return get_object_or_404(models.CourseGroup, code=self.kwargs['coursegroup_code'])

    def get_course_group_member(self):
        return get_object_or_404(models.CourseGroupMember, user=self.request.user)

    def get_course_group_session_today(self, course_group):
        today = timezone.now().date()
        # Retrieve the CourseGroupSession instance that matches the given CourseGroup and the current date
        return models.CourseGroupSession.objects.filter(course_group=course_group, date=today).first()

    def get_queryset(self):
        course_group = self.get_course_group()
        course_group_member = self.get_course_group_member()

        # Retrieve the Attendance instances that match the CourseGroup and CourseGroupMember
        queryset = models.Attendance.objects.filter(
            course_group_member=course_group_member,
            course_group_session__course_group=course_group
        )
        return queryset

    def create_course_group_session_if_not_exist(self, course_group):
        today = timezone.now().date()
        # Retrieve or create the CourseGroupSession instance for the given CourseGroup and current date
        course_group_session, created = models.CourseGroupSession.objects.get_or_create(
            course_group=course_group,
            date=today,
        )
        return course_group_session

    def perform_create(self, serializer):
        course_group = self.get_course_group()
        course_group_member = self.get_course_group_member()

        # Create or get the CourseGroupSession instance for the current date
        course_group_session = self.create_course_group_session_if_not_exist(course_group)

        # Create an Attendance instance with the check-in value set to the current time
        serializer.save(course_group_member=course_group_member, course_group_session=course_group_session)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
