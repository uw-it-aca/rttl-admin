from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rttl_admin.views.api import json_response, error_response
from logging import getLogger

logger = getLogger(__name__)


class UserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pass

    def patch(self, request, *args, **kwargs):
        pass

    def get(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass


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
