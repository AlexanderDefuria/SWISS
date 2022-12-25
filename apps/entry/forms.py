from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from apps.entry.models import *
from apps.entry.widgets import *


class MatchScoutForm(forms.Form):
    template_name = 'entry/components/forms/matchscout.html'

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event', None)
        super(MatchScoutForm, self).__init__(*args, **kwargs)

    @staticmethod
    def grouping(group_name, objects, subgroup=None):
        for i in objects:
            i.subgroup = subgroup
            i.group = group_name
        return objects

    def clean_match_number(self):
        self.get_context()
        match_number = self.cleaned_data['match_number']
        try:
            if Schedule.objects.get(match_number=match_number, event=self.event).completed:
                raise ValidationError("Match has already been completed.")
        except Exception as e:
            raise ValidationError("Match is not in schedule.")

        return match_number

    match_number = forms.IntegerField(min_value=0, max_value=255)
    on_field = forms.BooleanField(widget=BooleanWidget(), label='Is Robot Present?', required=False)
    preloaded_balls = forms.BooleanField(widget=BooleanWidget(image='SplitColourCargo.png'), label='Ball Preloaded', required=False)
    # TODO Starting Position WIDGET Do this widget without the numerical inputs actually showing

    # AUTO
    auto_route = forms.IntegerField(widget=widgets.Select(choices=[
                    (1, "foo"),
                    (2, "bar")
                ]), label='Autonomous Route')
    baseline = forms.BooleanField(widget=BooleanWidget(image='AllTarmacs.png'), label='Exit Tarmac', required=False)
    upper_auto = forms.IntegerField(widget=TickerWidget(image='HubUpper.png'), initial=0)
    lower_auto = forms.IntegerField(widget=TickerWidget(image='HubLower.png'), initial=0)
    missed_balls_auto = forms.IntegerField(widget=TickerWidget(image='MissedIcon.png'), initial=0)
    auto_fouls = forms.IntegerField(widget=widgets.Select(choices=[
                    (1, "foo"),
                    (2, "bar")
                ]), label='Auto Fouls')
    auto_comment = forms.CharField(
                    widget=widgets.Textarea(attrs={'rows': 2, 'cols': 50, 'placeholder': 'Auto Notes'}),
                    label="Auto Notes",
                    required=False
                )

    # TELEOP
    upper = forms.IntegerField(widget=TickerWidget(image='HubUpper.png'), initial=0)
    lower = forms.IntegerField(widget=TickerWidget(image='HubLower.png'), initial=0)
    missed_balls = forms.IntegerField(widget=TickerWidget(image='MissedIcon.png'), initial=0)
    intake_type = forms.IntegerField(widget=widgets.Select(choices=[
                    (1, "foo"),
                    (2, "bar")
                ]), label='Intake Type')
    under_defense = forms.IntegerField(widget=widgets.Select(choices=[
                    (1, "foo"),
                    (2, "bar")
                ]), label='Performance Under Defence')
    defended_by = forms.IntegerField(widget=widgets.NumberInput, required=False)
    offensive_fouls = forms.IntegerField(widget=widgets.Select(choices=[
                    (1, "foo"),
                    (2, "bar")
                ]), label='Offense Fouls')

    # DEFENSE
    defense_played = forms.BooleanField(widget=BooleanWidget(), label='Played Defense?', required=False)
    team_defended = forms.IntegerField(widget=widgets.NumberInput, required=False)  # TODO Can this now become a popup?
    defense_time = forms.IntegerField(widget=StopWatchWidget(), label="Defense Stopwatch", initial=0)
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
    climb_attempts = forms.IntegerField(widget=TickerWidget(), label='Climb Attempts', initial=0)
    climb_comments = forms.CharField(
                    widget=widgets.Textarea(attrs={'rows': 2, 'cols': 50, 'placeholder': 'Auto Notes'}),
                    label="Climb Performance Comment",
                    required=False
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
    yellow_card = forms.BooleanField(widget=BooleanWidget(), label='Yellow Card Given', required=False)
    comment = forms.CharField(
                    widget=widgets.Textarea(attrs={'rows': 4, 'cols': 50, 'placeholder': 'Auto Notes'}),
                    label="Comments",
                    required=False
                )

    grouping("PRE-MATCH", [match_number, on_field, preloaded_balls])
    grouping("AUTONOMOUS", [baseline, auto_route, auto_fouls])
    grouping("AUTONOMOUS", [upper_auto, lower_auto, missed_balls_auto], subgroup="Power Port Goals")
    grouping("TELEOP - OFFENSE", [intake_type, under_defense, defended_by, offensive_fouls])
    grouping("TELEOP - OFFENSE", [upper, lower, missed_balls], subgroup="Power Port Goals")
    grouping("TELEOP - DEFENSE", [defense_played, team_defended, defense_rating, defense_fouls, able_to_push])
    grouping("ENDGAME", [lock_status, endgame_action, climb_attempts, climb_comments])
    grouping("MORE", [fouls_hp, fouls_driver, yellow_card, comment])

    class Meta:
        model = Match()
        widgets = {'auto_high': TickerWidget()}

