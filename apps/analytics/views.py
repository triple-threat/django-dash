from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView, View
from django.utils.decorators import method_decorator

from analytics.calculator import MetricDataFetcher


class MetricView(TemplateView):
    template_name = 'analytis/metric.html'

    def get(self, request, metric_name, **kwargs):
        redis_data = Calculator(metric_name).get_redis_data()
        pass
