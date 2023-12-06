from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Protocol, Type

from django.core.exceptions import ImproperlyConfigured
from django.db.models import Model

from model_hooks.events import HookEvent


class DecoratedFunc(Protocol):

    def __call__(self, instance: Model, payload: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        ...


@dataclass
class HookData:
    func: DecoratedFunc
    tag: Optional[str] = None
    serializer: Optional[Callable[[Any], Dict[str, Any]]] = None


model_hooks = {}


def model_hook(model: Type[Model], event: HookEvent, tag: Optional[str] = None,
               serializer: Optional[Callable[[Any], Dict[str, Any]]] = None):

    def decorator(func: DecoratedFunc):
        if event.model is not None and event.model != model:
            raise ImproperlyConfigured(f"Event {event} cannot be used together with {model}")

        model_hooks.setdefault((model, event), []).append(HookData(
            func=func,
            tag=tag,
            serializer=serializer
        ))
        return func

    return decorator
