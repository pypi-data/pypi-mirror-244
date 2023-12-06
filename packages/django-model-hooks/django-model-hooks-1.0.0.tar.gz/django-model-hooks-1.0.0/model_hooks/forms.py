import operator

from django import forms

from model_hooks.events import hook_events
from model_hooks.models import Hook


class HookForm(forms.ModelForm):

    event = forms.ChoiceField(choices=())

    class Meta:
        model = Hook
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['event'].choices = (('', '----------'),) + tuple(
            (event.name, event.name)
            for event in sorted(hook_events, key=operator.attrgetter('name'))
        )
