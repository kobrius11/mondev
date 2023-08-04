from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .. import models 
## please review regarding issue 37
# find if current user is a CourseGroupMember of the given CourseGroup
# question does attendence object only is created when user checks in ? (then check_in cant be None and this will not work)
class CheckIn(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        course_group = models.CourseGroup.objects.filter(slug=self.kwargs['slug'])
        return super().get_queryset()

    def perform_create(self, serializer):
        pass

    def get(self, request, format=None):
        pass
        


# test_func that user is CourseGroupMember of the given Attendance record
# set checkout to now
