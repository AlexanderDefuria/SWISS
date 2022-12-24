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


class MatchScoutForm(forms.Form):
    template_name = 'entry/components/forms/matchscout.html'

    @staticmethod
    def grouping(group_name, objects, subgroup=None):
        for i in objects:
            i.subgroup = subgroup
            i.group = group_name
        return objects

    match_number = forms.IntegerField(min_value=0, max_value=255)
    on_field = forms.BooleanField(widget=BooleanWidget(), label='Is Robot Present?')
    preloaded_balls = forms.BooleanField(widget=BooleanWidget(image='SplitColourCargo.png'), label='Ball Preloaded')
    # TODO Starting Position WIDGET Do this widget without the numerical inputs actually showing

    # AUTO
    auto_route = forms.IntegerField(widget=widgets.Select(choices=[
                    (1, "foo"),
                    (2, "bar")
                ]), label='Autonomous Route')
    baseline = forms.BooleanField(widget=BooleanWidget(image='AllTarmacs.png'), label='Exit Tarmac')
    auto_high = forms.IntegerField(widget=TickerWidget(image='HubUpper.png'))
    auto_low = forms.IntegerField(widget=TickerWidget(image='HubLower.png'))
    missed_balls_auto = forms.IntegerField(widget=TickerWidget(image='MissedIcon.png'))
    auto_fouls = forms.IntegerField(widget=widgets.Select(choices=[
                    (1, "foo"),
                    (2, "bar")
                ]), label='Auto Fouls')
    auto_notes = forms.CharField(
                    widget=widgets.Textarea(attrs={'rows': 2, 'cols': 50, 'placeholder': 'Auto Notes'}),
                    label="Auto Notes"
                )

    # TELEOP
    upper = forms.IntegerField(widget=TickerWidget(image='HubUpper.png'))
    lower = forms.IntegerField(widget=TickerWidget(image='HubLower.png'))
    missed_balls = forms.IntegerField(widget=TickerWidget(image='MissedIcon.png'))
    intake_type = forms.IntegerField(widget=widgets.Select(choices=[
                    (1, "foo"),
                    (2, "bar")
                ]), label='Intake Type')
    under_defense = forms.IntegerField(widget=widgets.Select(choices=[
                    (1, "foo"),
                    (2, "bar")
                ]), label='Performance Under Defence')
    defended_by = forms.IntegerField(widget=widgets.NumberInput)
    offensive_fouls = forms.IntegerField(widget=widgets.Select(choices=[
                    (1, "foo"),
                    (2, "bar")
                ]), label='Offense Fouls')

    # DEFENSE
    defense_played = forms.BooleanField(widget=BooleanWidget(), label='Played Defense?')
    team_defended = forms.IntegerField(widget=widgets.NumberInput) # TODO Can this now become a popup?
    defense_rating = forms.IntegerField(widget=widgets.Select(choices=[
                    (1, "foo"),
                    (2, "bar")
                ]), label='Quality of Defense')
    defense_fouls = forms.IntegerField(widget=widgets.Select(choices=[
                    (1, "foo"),
                    (2, "bar")
                ]), label='Defense Fouls')
    able_to_push = forms.IntegerField(widget=widgets.Select(choices=[
                    (1, "foo"),
                    (2, "bar")
                ]), label='Ability to Push')

    # ENDGAME
    lock_status = forms.IntegerField(widget=widgets.Select(choices=[
                    (1, "foo"),
                    (2, "bar")
                ]), label='Field Timeout Position (t=+5s')
    endgame_action = forms.IntegerField(widget=widgets.Select(choices=[
                    (1, "foo"),
                    (2, "bar")
                ]), label='Climb Height')
    climb_attempts = forms.IntegerField(widget=TickerWidget(), label='Climb Attempts')
    climb_comments = forms.CharField(
                        widget=widgets.Textarea(attrs={'rows': 2, 'cols': 50, 'placeholder': 'Auto Notes'}),
                        label="Climb Performance Comment"
                    )

    # MORE
    fouls_hp = forms.IntegerField(widget=widgets.Select(choices=[
                    (1, "foo"),
                    (2, "bar")
                ]), label='Human Player Fouls')
    fouls_driver = forms.IntegerField(widget=widgets.Select(choices=[
                    (1, "foo"),
                    (2, "bar")
                ]), label='Driver/Coach Fouls')
    yellow_card = forms.BooleanField(widget=BooleanWidget(), label='Yellow Card Given')
    comment = forms.CharField(
                        widget=widgets.Textarea(attrs={'rows': 4, 'cols': 50, 'placeholder': 'Auto Notes'}),
                        label="Comments"
                    )

    grouping("PRE-MATCH", [match_number, on_field, preloaded_balls])
    grouping("AUTONOMOUS", [baseline, auto_route, auto_fouls])
    grouping("AUTONOMOUS", [auto_high, auto_low, missed_balls_auto], subgroup="Power Port Goals")
    grouping("TELEOP - OFFENSE", [intake_type, under_defense, defended_by, offensive_fouls])
    grouping("TELEOP - OFFENSE", [upper, lower, missed_balls], subgroup="Power Port Goals")
    grouping("TELEOP - DEFENSE", [defense_played, team_defended, defense_rating, defense_fouls, able_to_push])
    grouping("ENDGAME", [lock_status, endgame_action, climb_attempts, climb_comments])
    grouping("MORE", [fouls_hp, fouls_driver, yellow_card, comment])

    class Meta:
        model = Match()
        widgets = {'auto_high': TickerWidget()}

