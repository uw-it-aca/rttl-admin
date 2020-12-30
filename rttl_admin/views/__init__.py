from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from rttl_admin.decorators import group_required


@method_decorator(group_required(settings.RTTL_ADMIN_GROUP), name='dispatch')
class AdminView(View):
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self._params(request))

    def _params(self, request):
        return {}


class HomeView(AdminView):
    template_name = 'rttl_admin/home.html'



