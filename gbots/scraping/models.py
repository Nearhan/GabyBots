from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from dynamic_scraper.models import Scraper, SchedulerRuntime


class WeakForeignKey(models.ForeignKey):
    """
    Loosly couple this to a foreign table to prevent cascading deletes, invalid ids, and to permit missing ids.
    """
    def __init__(self, *args, **kwargs):
        kwargs.update(blank=True, null=True, on_delete=models.SET_NULL)
        super(WeakForeignKey, self).__init__(*args, **kwargs)

# Allow South to introspect these fields
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^scraping\.models\.WeakForeignKey"])

# Sample code to dynamically delete active scrapers when the scraper is deleted from the admin interface
#@receiver(pre_delete)
#def pre_delete_handler(sender, instance, using, **kwargs):
#    ....
#
#    if isinstance(instance, Article):
#        if instance.checker_runtime:
#            instance.checker_runtime.delete()
#
#pre_delete.connect(pre_delete_handler)


class WebSource(models.Model):
    scraper = WeakForeignKey(Scraper)
    scraper_runtime = WeakForeignKey(SchedulerRuntime)
    name = models.CharField(max_length=200)
    url = models.URLField()

    def __unicode__(self):
        return self.name


class Article(models.Model):
    checker_runtime = WeakForeignKey(SchedulerRuntime)
    # This name is significant to DjangoWriterPipeline
    source = models.ForeignKey(WebSource)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    url = models.URLField()

    def __unicode__(self):
        return self.title
