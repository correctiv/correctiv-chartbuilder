from django.conf.urls import url

from .api_views import ChartAPIView

urlpatterns = [
    url(r'^charts/(?P<pk>[0-9]+)/$', ChartAPIView.as_view(), name='chartbuilder-api-detailview'),
]
