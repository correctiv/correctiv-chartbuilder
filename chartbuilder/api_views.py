from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework import serializers
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework import parsers

from .models import Chart


class JSONSerializerField(serializers.Field):
    """ Serializer for JSONField -- required to make field writable"""
    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        return value


class ChartSerializer(serializers.ModelSerializer):
    chart_settings = JSONSerializerField()

    class Meta:
        model = Chart
        fields = ('title', 'csv_data', 'chart_settings',
                  'svg', 'width', 'height')


def get_svg_parser(fields):
    class Impl(parsers.JSONParser):
        media_type = 'application/json'

        def parse(self, *args, **kwargs):
            ret = super(Impl, self).parse(*args, **kwargs)
            ret['svg'] = SimpleUploadedFile(name='chart.svg', content=ret['svg'].encode('utf-8'))
            return ret
    return Impl


class ChartAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ChartSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    parser_classes = [get_svg_parser(('svg',))]

    def get_queryset(self):
        qs = Chart.objects.filter(is_public=True)
        if self.request.user.is_authenticated():
            if self.request.user.has_perm('chartbuilder.view_chart'):
                qs = Chart.objects.all()
        return qs
