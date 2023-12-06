from django.contrib import admin

from model_hooks.forms import HookForm
from model_hooks.models import Hook, HookLog


class HookAdmin(admin.ModelAdmin):
    form = HookForm


admin.site.register(Hook, HookAdmin)


class HookLogAdmin(admin.ModelAdmin):

    date_hierarchy = 'created'

    fields = ('target', 'hook', 'payload', 'success', 'errors')

    list_display = ('created', 'target', 'hook', 'success')

    list_filter = ('hook', 'success')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('hook')

    def target(self, obj):
        return obj.content_object

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(HookLog, HookLogAdmin)
