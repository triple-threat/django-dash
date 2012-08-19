import datetime

from django.views.generic.base import TemplateView, View

from analytics.calculator import MetricDataFetcher


class MetricView(TemplateView):
    template_name = 'analytics/metric.html'

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
