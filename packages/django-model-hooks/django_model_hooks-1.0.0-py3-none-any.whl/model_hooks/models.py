from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Hook(models.Model):

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='hooks')

    event = models.CharField(max_length=32)

    tag = models.CharField(max_length=32, blank=True)

    parameters = models.JSONField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('content_type', 'event', 'tag'),
                name='Unique constraint on content_type, event and tag',
                condition=~models.Q(tag='')
            )
        ]
        ordering = ('content_type', 'event', 'tag')

    def __str__(self):
        return f'{self.content_type} - {self.event}'


class HookLog(models.Model):

    created = models.DateTimeField(auto_now=True)

    content_object = GenericForeignKey()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='hook_logs')

    object_id = models.CharField(max_length=100)

    hook = models.ForeignKey(Hook, on_delete=models.CASCADE, related_name='logs')

    payload = models.TextField(blank=True)

    success = models.BooleanField(default=False)

    errors = models.TextField(blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.hook} - {self.content_object}'
