import datetime

from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator

from analytics.calculator import MetricDataFetcher
from util.decorators import superuser_required


class MetricView(TemplateView):
    template_name = 'analytics/metric.html'

    @method_decorator(superuser_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MetricView, self).dispatch(request, *args, **kwargs)

    def get(self, request, metric_name, hours_ago, **kwargs):
        redis_data = MetricDataFetcher(metric_name, hours_ago).get_redis_data()
        context = {
            'metric_name': metric_name,
            'hours_ago': hours_ago,
            'redis_data': [x[1] for x in redis_data.items()],
            'start': datetime.datetime.now(),
        }
        return self.render_to_response(context)

metric = MetricView.as_view()
