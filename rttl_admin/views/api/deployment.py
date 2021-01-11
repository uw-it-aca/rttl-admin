from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer
from rttl_admin.models import Deployment, Course
from logging import getLogger

logger = getLogger(__name__)


class DeploymentSerializer(ModelSerializer):
    def create(self, validated_data):
        course = validated_data['course']
        key = ''
        deployment, created = Deployment.objects.get_or_create(
            course=course, key=key, defaults={
                'message': validated_data.get('message')})
        return deployment

    class Meta:
        model = Deployment


class DeploymentView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            request.data['course'] = Course.objects.get(pk=kwargs['course_id'])
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = DeploymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        try:
            request.data['course'] = Course.objects.get(pk=kwargs['course_id'])
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        deployment_id = kwargs.get('deployment_id')
        if deployment_id:
            try:
                serializer = DeploymentSerializer(
                    Deployment.objects.get(course=course, pk=deployment_id))
            except Deployment.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = DeploymentSerializer(
                Deployments.objects.filter(course=course), many=True)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        try:
            request.data['course'] = Course.objects.get(pk=kwargs['course_id'])
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        deployment_id = kwargs.get('deployment_id')
        try:
            deployment = Deployment.objects.get(course=course,
                                                pk=deployment_id)
            deployment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Deployment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
