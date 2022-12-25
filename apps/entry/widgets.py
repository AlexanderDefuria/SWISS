from django import forms
from django.template import loader
from django.utils.safestring import mark_safe


class TickerWidget(forms.Widget):
    template_name = 'entry/components/widgets/ticker.html'
    image = ''

    def __init__(self, image=''):
        super().__init__()
        self.image = image

    def get_context(self, name, value, attrs=None, **kwargs):
        return {'widget': {
            'name': name,
            'value': value,
            'image': self.image
        }}

    def render(self, name, value, attrs=None, **kwargs):
        context = self.get_context(name, value, attrs, **kwargs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)


class BooleanWidget(TickerWidget):
    def format_value(self, value):
        value = value[0]
        return super(self, value)

    template_name = 'entry/components/widgets/boolean.html'


class StopWatchWidget(forms.Widget):
    template_name = 'entry/components/widgets/stopwatch.html'

    def get_context(self, name, value, attrs=None, **kwargs):
        return {'widget': {
            'name': name,
            'value': value
        }}

    def render(self, name, value, attrs=None, **kwargs):
        context = self.get_context(name, value, attrs, **kwargs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)
