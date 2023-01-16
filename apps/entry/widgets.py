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


class LocationWidget(forms.MultiWidget):
    template_name = 'entry/components/widgets/location-picker.html'

    def __init__(self, attrs=None):
        widgets = (
            forms.NumberInput(),
            forms.NumberInput()
        )
        super(LocationWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            data = value.split(',')
            return data
        else:
            return [0.0, 0.0]

    def format_value(self, value):
        if value:
            return 'X: %s, Y: %s' % (value[0], value[1])
        return [0.0, 0.0]


class LocationField(forms.MultiValueField):
    def __init__(self, required=True, widget=None, label=None, initial=None):
        fields = (
            forms.FloatField(initial=1.0, min_value=0, max_value=1),
            forms.FloatField(initial=1.0, min_value=0, max_value=1)
        )
        super(LocationField, self).__init__(fields, required=required, widget=widget, label=label, initial=initial)

    def compress(self, data_list):
        return data_list
