import datetime
import logging
import pprint
from io import StringIO
from typing import Any, Dict, List, Optional, Tuple, Type

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model
from django.utils.timezone import now

from model_hooks.decorators import HookData, model_hooks
from model_hooks.events import HookEvent
from model_hooks.models import Hook, HookLog


logger = logging.getLogger(__name__)


def find_and_fire_hooks(sender: Type[Model], event: HookEvent, instance: Model):
    for hook, hook_data in get_hooks_to_fire(sender, event):
        logger.info(f'Firing hook {hook} for function {hook_data.func.__name__}')
        payload = hook_data.serializer(instance) if hook_data.serializer else None
        try:
            hook_data.func(instance, payload, **(hook.parameters or {}))
            log_hook(instance, hook, payload)
        except Exception as exc:
            logger.error(f'Error firing hook {hook} for function {hook_data.func.__name__}: {exc}')
            log_hook(instance, hook, payload, success=False, errors=str(exc))
        finally:
            log_prune(hook)


def get_hooks_to_fire(model: Type[Model], event: HookEvent) -> List[Tuple[Hook, HookData]]:
    available_hooks = model_hooks.get((model, event), [])
    if not available_hooks:
        return []

    hooks_to_fire = []
    content_type = ContentType.objects.get_for_model(model)
    for hook in content_type.hooks.filter(event=event).all():
        for hook_data in available_hooks:
            if (not hook.tag and not hook_data.tag) or hook.tag == hook_data.tag:
                hooks_to_fire.append((hook, hook_data))
    return hooks_to_fire


def log_hook(instance: Model, hook: Hook, payload: Optional[Dict[str, Any]] = None, success: Optional[bool] = True,
             errors: Optional[str] = ''):
    fh = StringIO()
    pprint.pprint(payload, stream=fh, width=1)
    HookLog.objects.create(
        content_object=instance,
        hook=hook,
        payload=fh.getvalue(),
        success=success,
        errors=errors
    )


def log_prune(hook: Hook):
    offset = now() - datetime.timedelta(days=getattr(settings, 'HOOK_LOG_RETENTION_DAYS', 7))
    hook.logs.filter(created__lt=offset).delete()
