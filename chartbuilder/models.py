# -*- encoding: utf-8 -*-
import os
import hashlib

from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils.encoding import force_bytes, python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

try:
    from cms.models.pluginmodel import CMSPlugin
except ImportError:
    CMSPlugin = None

from jsonfield import JSONField


class OverwriteStorage(FileSystemStorage):
    '''
    Muda o comportamento padrão do Django e o faz sobrescrever arquivos de
    mesmo nome que foram carregados pelo usuário ao invés de renomeá-los.
    '''
    def get_available_name(self, name):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


def chart_file_path(instance=None, filename=None):
    tmppath = ['charts']
    root, ext = os.path.splitext(filename)
    filehash = hashlib.md5(force_bytes(instance.slug) +
                           force_bytes(instance.pk)).hexdigest()
    filehash_start = filehash[:2]
    tmppath.append(filehash_start)
    filehash_middle = filehash[2:4]
    tmppath.append(filehash_middle)
    tmppath.append(str(instance.pk))
    new_filename = '%s.svg' % instance.slug
    tmppath.append(new_filename)
    return os.path.join(*tmppath)


@python_2_unicode_compatible
class Chart(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_public = models.BooleanField(default=False)

    csv_data = models.TextField(blank=True)
    chart_settings = JSONField(blank=True)

    svg = models.FileField(null=True, blank=True,
                           upload_to=chart_file_path,
                           storage=OverwriteStorage())
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    customised = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('chart')
        verbose_name_plural = _('charts')
        ordering = ('-created_at',)

    def __str__(self):
        return self.title


if CMSPlugin is not None:
    @python_2_unicode_compatible
    class DisplayChartPlugin(CMSPlugin):
        """
        CMS Plugin for displaying custom entries
        """

        chart = models.ForeignKey(Chart)

        def __str__(self):
            return _('Chart %s') % self.chart
