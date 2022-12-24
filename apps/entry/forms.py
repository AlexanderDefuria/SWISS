from django import forms
from django.core.validators import RegexValidator
from django.forms import widgets
from django.template import loader
from django.utils.safestring import mark_safe
from apps.entry.models import *

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
    template_name = 'entry/components/widgets/boolean.html'

class MultiTickerWidget(forms.MultiWidget):

    def __init__(self, widgets=None, attrs=None):
        widgets = [
            TickerWidget(image='HubUpper.png'),
            TickerWidget(),
        ]
        super().__init__(widgets, attrs)


    def decompress(self, value):
        pass

class MultiTickerField(forms.MultiValueField):

    def __init__(self, **kwargs):
        # Define one message for all fields.
        error_messages = {
            'incomplete': 'Enter a country calling code and a phone number.',
        }
        # Or define a different message for each field.
        fields = [
            forms.IntegerField(
                error_messages={'incomplete': 'Enter a country calling code.'},
                validators=[
                    RegexValidator(r'^[0-9]+$', 'Enter a valid country calling code.'),
                ],
            ),
            forms.CharField(
                error_messages={'incomplete': 'Enter a phone number.'},
                validators=[RegexValidator(r'^[0-9]+$', 'Enter a valid phone number.')],
            ),
            forms.CharField(
                validators=[RegexValidator(r'^[0-9]+$', 'Enter a valid extension.')],
                required=False,
            ),
        ]
        super().__init__(
            error_messages=error_messages, fields=fields,
            require_all_fields=False, **kwargs
        )

    def compress(self, data_list):
        pass


class TestForm(forms.Form):
    template_name = 'entry/components/forms/experimental.html'

    match_number = forms.IntegerField(min_value=0, max_value=255)
    on_field = forms.BooleanField(widget=BooleanWidget(), label='Is Robot Present?')
    # Starting Position
    preloaded_balls = forms.BooleanField(widget=BooleanWidget(image='SplitColourCargo.png'), label='Ball Preloaded')

    # AUTO
    auto_route = forms.IntegerField(widget=widgets.Select(choices=[
        (1, "foo"),
        (2, "bar")
    ]), label='Autonomous Route')
    baseline = forms.BooleanField(widget=BooleanWidget(image='SplitColourCargo.png'), label='Ball Preloaded')
    auto_high = forms.IntegerField(widget=TickerWidget(image='HubUpper.png'), label='Power Port Goals')
    auto_low = forms.IntegerField(widget=TickerWidget(image='HubLower.png'))
    missed_balls_auto = forms.IntegerField(widget=TickerWidget(image='MissedIcon.png'), label='Missed Balls')
    auto_fouls = forms.IntegerField(widget=widgets.Select(choices=[
        (1, "foo"),
        (2, "bar")
    ]), label='Auto Fouls')
    auto_notes = forms.CharField(widget=widgets.Textarea(attrs={'rows': 2, 'cols': 50, 'placeholder': 'Auto Notes'}), label="Auto Notes")



    class Meta:
        model = Match()
        widgets = {'auto_high': TickerWidget()}

