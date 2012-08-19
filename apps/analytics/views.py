# Promise.ly -- social commitment platform
#
# Copyright (C) 2012  Promise.ly authors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import datetime

from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator

from analytics.calculator import MetricDataFetcher
from util.decorators import superuser_required


class MetricView(TemplateView):
    """
    Displays to admin (superuser) core metrics like signup (# of signups), promise (# of promises), support (# of support actions)
    over time by minute granularity. Extensible to take any of the metrics from the event app.
    """
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
