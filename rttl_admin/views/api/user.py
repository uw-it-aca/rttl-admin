from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer
from uw_canvas.users import Users as Canvas
from restclients_core.exceptions import DataFailureException
from rttl_admin.models import User
from logging import getLogger

logger = getLogger(__name__)


class UserSerializer(ModelSerializer):
    def create(self, validated_data):
        login = validated_data['username']
        canvas_user = Canvas().get_user('sis_login_id:{}'.format(login))
        user, created = User.objects.get_or_create(username=login, defaults={
            'first_name': canvas_user.name})
        return user

    class Meta:
        model = User
        fields = '__all__'


class UserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            except DataFailureException as ex:
                return Response(ex.msg, status=ex.status)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        if user_id:
            try:
                serializer = UserSerializer(User.objects.get(pk=user_id))
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = UserSerializer(User.objects.all(), many=True)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        user_id = kwargs['user_id']
        try:
            user = User.objects.get(pk=user_id)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserRoleView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pass

    def get(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass


class UserCourseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pass

    def get(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass
