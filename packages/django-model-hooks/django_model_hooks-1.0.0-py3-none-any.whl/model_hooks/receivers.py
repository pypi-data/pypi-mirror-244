from typing import Type

from django.db.models import Model
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils.module_loading import autodiscover_modules

from model_hooks.events import create_event, delete_event, update_event, HookEvent
from model_hooks.signals import hook_event
from model_hooks.utils import find_and_fire_hooks


autodiscover_modules('model_hooks_registry')


@receiver(post_save)
def handle_save(sender, created: bool, instance: Model, **kwargs):
    event = create_event if created else update_event
    find_and_fire_hooks(sender, event, instance)


@receiver(post_delete)
def handle_delete(sender, instance: Model, **kwargs):
    find_and_fire_hooks(sender, delete_event, instance)


@receiver(hook_event)
def handle_event(sender, model: Type[Model], instance: Model, event: HookEvent, **kwargs):
    find_and_fire_hooks(model, event, instance)
