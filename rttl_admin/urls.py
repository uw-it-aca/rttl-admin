from django.urls import re_path
from rttl_admin.views.api.user import UserView
from rttl_admin.views.api.course import CourseView
from rttl_admin.views.api.image import ImageView
from rttl_admin.views.api.deployment import DeploymentView

urlpatterns = [
    re_path(r'api/v1/users/?(?P<user_id>[0-9]+)$', UserView.as_view()),
    re_path(r'api/v1/courses/?(?P<course_id>[0-9]+)$', CourseView.as_view()),
    re_path(r'api/v1/images/?(?P<image_id>[0-9]+)$', ImageView.as_view()),
    re_path(r'api/v1/courses/(?P<course_id>[0-9]+)/deployments/?'
            r'(?P<deployment_id>[0-9]+)$', DeploymentView.as_view()),
]
