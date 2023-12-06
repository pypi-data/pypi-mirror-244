from typing import Optional, Type

from django.db.models import Model


hook_events = set()


class HookEvent:

    name: str

    model: Optional[Type[Model]] = None

    def __init__(self, name: str, model: Optional[Type[Model]] = None):
        self.name = name
        self.model = model
        hook_events.add(self)

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    def __hash__(self):
        parts = list(filter(None, [self.name, self.model._meta.label if self.model else None]))
        return hash("".join(parts))


create_event = HookEvent('create')
update_event = HookEvent('update')
delete_event = HookEvent('delete')
