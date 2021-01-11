from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer
from uw_canvas.courses import Courses as Canvas
from restclients_core.exceptions import DataFailureException
from rttl_admin.models import Course
from logging import getLogger
import random
import string

logger = getLogger(__name__)


class CourseSerializer(ModelSerializer):
    def create(self, validated_data):
        sis_course_id = validated_data['sis_course_id']
        canvas_course = Canvas().get_course_by_sis_id(sis_course_id)

        key = sis_course_id.lower().replace(' ', '-')
        course, created = Course.objects.get_or_create(key=key, defaults={
            'sis_course_id': sis_course_id,
            'contact_name': validated_data.get('contact_name'),
            'contact_email': validated_data.get('contact_email'),
            'name': canvas_course.name,
            'code': canvas_course.code,
            'hub_url': '{}/{}'.format(settings.JHUB_URL, key),
            'hub_token': ''.join(random.SystemRandom().choice(
                string.hexdigits) for _ in range(32))})

        # TODO: Create UserCourse
        # TODO: Create CourseSettings model
        # TODO: Create CourseExtraEnv model(s)
        # TODO: Create CourseGitPullerTarget model

        return course

    class Meta:
        model = Course
        exclude = ['hub_token']


class CourseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # TODO: implement batch create if request.data is CSV
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            except DataFailureException as ex:
                return Response(ex.msg, status=ex.status)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        course_id = kwargs['course_id']
        try:
            course = Course.objects.get(pk=course_id)

            # TODO

        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, *args, **kwargs):
        course_id = kwargs.get('course_id')
        if course_id:
            try:
                serializer = CourseSerializer(Course.objects.get(pk=course_id))
            except Course.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = CourseSerializer(Course.objects.all(), many=True)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        course_id = kwargs['course_id']
        try:
            course = Course.objects.get(pk=course_id)
            course.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
