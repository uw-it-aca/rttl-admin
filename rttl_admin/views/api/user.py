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
        username = validated_data['username']
        canvas_user = Canvas().get_user('sis_login_id:{}'.format(username))

        user, c = User.objects.get_or_create(username=username, defaults={
            'first_name': canvas_user.name})
        user.save()
        return user

    class Meta:
        model = User
        fields = '__all__'


class UsersView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


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
        user_id = kwargs['user_id']
        try:
            serializer = UserSerializer(User.objects.get(pk=user_id))
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

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
