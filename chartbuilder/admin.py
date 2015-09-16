from django.contrib import admin
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import url

from .models import Chart


class ChartAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'created_at',
                    'creator',)
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = 'created_at'
    raw_id_fields = ('creator',)

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'is_public', 'creator', 'created_at',),
        }),
        (_('Advanced'), {
            'fields': ('csv_data', 'chart_settings',
                       'svg', 'width', 'height', 'customised'),
            'classes': ('collapse', 'collapse-closed')
        }),
    )

    def get_urls(self):
        urls = super(ChartAdmin, self).get_urls()
        my_urls = [
            url(r'^chart-form/$',
                self.admin_site.admin_view(self.get_chart_form),
                name='chartbuilder-admin-get_chart_form'),
        ]
        return my_urls + urls

    def get_chart_form(self, request):
        return TemplateResponse(request, 'chartbuilder/chartbuilder.html')

admin.site.register(Chart, ChartAdmin)
