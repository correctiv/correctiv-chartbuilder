from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import DisplayChartPlugin


@plugin_pool.register_plugin
class DisplayChartCMSPlugin(CMSPluginBase):
    """
    Plugin for including a selection of entries
    """
    module = _('Charts')
    name = _('Render Chart')
    model = DisplayChartPlugin
    render_template = 'chartbuilder/plugins/default.html'
    text_enabled = True
    raw_id_fields = ('chart',)

    def render(self, context, instance, placeholder):
        """
        Update the context with plugin's data
        """
        context = super(DisplayChartCMSPlugin, self).render(
            context, instance, placeholder)
        context['object'] = instance
        return context

    def icon_src(self, instance):
        if instance.chart.svg:
            return instance.chart.svg.url
        return settings.STATIC_URL + "cms/img/icons/plugins/link.png"
