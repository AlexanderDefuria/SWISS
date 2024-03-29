from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.forms import widgets
from apps.entry.models import *
from apps.entry.widgets import *


def grouping(group_name, objects, subgroup=None):
    for i in objects:
        i.subgroup = subgroup
        i.group = group_name
    return objects


class MatchScoutForm(forms.Form):
    template_name = 'entry/components/forms/scout.html'

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event', None)
        self.ownership = kwargs.pop('ownership', None)
        super(MatchScoutForm, self).__init__(*args, **kwargs)

    def clean_match_number(self):
        self.get_context()
        match_number = self.cleaned_data['match_number']
        try:
            if Result.objects.get(match__match_number=match_number,
                                  ownership=self.ownership,
                                  event=self.event).completed:
                raise ValidationError("Match has already been completed.")
        except Result.DoesNotExist as e:
            return match_number

        return match_number

    def clean_grid_value(self):
        return int(str(self.cleaned_data['preloaded_balls']), 2)

    # PRE GAME
    match_number = forms.IntegerField(min_value=0, max_value=255)
    on_field = forms.BooleanField(widget=BooleanWidget(), label='Is Robot Present?', required=False)
    preloaded_balls = forms.BooleanField(widget=BooleanWidget(), label='Preloaded Balls', initial=0)

    # AUTO
    auto_placement = forms.IntegerField(widget=ConeCubeWidget(), label='', initial=0)
    auto_route = forms.IntegerField(widget=widgets.Select(choices=[
                    (0, "None"),
                    (1, "Yes, Simple"),
                    (2, "Yes, Complex")
                ]), label='Autonomous Route')
    auto_baseline = forms.BooleanField(widget=BooleanWidget(image='AllTarmacs.png'), label='Exit Tarmac', required=False)
    auto_fouls = forms.IntegerField(widget=widgets.Select(choices=[
                    (0, "None"),
                    (1, "Yes, Minor"),
                    (2, "Yes, Major")
                ]), label='Auto Fouls')
    auto_comment = forms.CharField(
                    widget=widgets.Textarea(attrs={'rows': 2, 'cols': 50, 'placeholder': 'Auto Notes'}),
                    label="Auto Notes",
                    required=False
                )
    auto_start = LocationField(widget=LocationWidget(), label="Location Field", initial=[0, 0])

    # TELEOP
    placement = forms.IntegerField(widget=ConeCubeWidget(), label='', initial=0)
    cycles = forms.IntegerField(widget=TickerWidget(), label='Teleop Cycles')
    intake_type = forms.IntegerField(widget=widgets.Select(choices=[
                    (0, "Did not Intake"),
                    (1, "Ground"),
                    (2, "Human"),
                    (3, "Both"),
                ]), label='Intake Type')
    under_defense = forms.IntegerField(widget=widgets.Select(choices=[
                    (0, "Not Defended"),
                    (1, "Played Poorly"),
                    (2, "Played Well"),
                ]), label='Performance Under Defence')
    defended_by = forms.IntegerField(widget=widgets.NumberInput, required=False)
    offensive_fouls = forms.IntegerField(widget=widgets.Select(choices=[
                    (0, "None"),
                    (1, "Yes, Minor"),
                    (2, "Yes, Major")
                ]), label='Offense Fouls')

    # DEFENSE
    defense_played = forms.BooleanField(widget=BooleanWidget(), label='Played Defense?', required=False)
    team_defended = forms.IntegerField(widget=widgets.NumberInput, required=False)  # TODO Can this now become a popup?
    defense_time = forms.IntegerField(widget=StopWatchWidget(), label="Defense Stopwatch", initial=0)
    defense_rating = forms.IntegerField(widget=widgets.Select(choices=[
                    (0, "Not Applicable"),
                    (1, "Attempted, Poor"),
                    (2, "Minor Annoyance"),
                    (3, "Good"),
                    (4, "Excellent"),
                    (5, "God-like"),
                ]), label='Quality of Defense')
    defense_fouls = forms.IntegerField(widget=widgets.Select(choices=[
                    (0, "None"),
                    (1, "Yes, Minor"),
                    (2, "Yes, Major")
                ]), label='Defense Fouls')
    able_to_push = forms.IntegerField(widget=widgets.Select(choices=[
                    (0, "N/A"),
                    (1, "Poorly"),
                    (2, "Well")
                ]), label='Ability to Push')

    # ENDGAME
    endgame_time = forms.IntegerField(widget=StopWatchWidget(), label="Time Spent Balancing", initial=0)
    endgame_action = forms.IntegerField(widget=widgets.Select(choices=[
                    (0, "No Attempt"),
                    (1, "Successful Balance"),
                    (2, "Unsuccessful Balance"),
                    (3, "Invalidated"),
                ]), label='Field Timeout Position (t=+5s')
    endgame_attempts = forms.IntegerField(widget=TickerWidget(), label='Climb Attempts', initial=0)
    endgame_comments = forms.CharField(
                    widget=widgets.Textarea(attrs={'rows': 2, 'cols': 50, 'placeholder': 'Auto Notes'}),
                    label="Climb Performance Comment",
                    required=False
                )

    # MORE
    fouls_hp = forms.IntegerField(widget=widgets.Select(choices=[
                    (0, "None"),
                    (1, "Yes"),
                    (2, "Yes, Repeatedly")
                ]), label='Human Player Fouls')
    fouls_driver = forms.IntegerField(widget=widgets.Select(choices=[
                    (0, "None"),
                    (1, "Yes"),
                    (2, "Yes, Repeatedly")
                ]), label='Driver/Coach Fouls')
    yellow_card = forms.BooleanField(widget=BooleanWidget(), label='Yellow Card Given', required=False)
    comment = forms.CharField(
                    widget=widgets.Textarea(attrs={'rows': 4, 'cols': 50, 'placeholder': 'Auto Notes'}),
                    label="Comments",
                    required=False
                )

    grouping("PRE-MATCH", [match_number, on_field, preloaded_balls])
    grouping("AUTONOMOUS", [auto_placement, auto_baseline, auto_route, auto_fouls])
    grouping("TELEOP - OFFENSE", [placement, cycles, intake_type, under_defense, defended_by, offensive_fouls])
    grouping("TELEOP - DEFENSE", [defense_played, team_defended, defense_rating, defense_fouls, able_to_push])
    grouping("ENDGAME", [endgame_time, endgame_action, endgame_attempts, endgame_comments])
    grouping("MORE", [fouls_hp, fouls_driver, yellow_card, comment])

    class Meta:
        model = Match()
        widgets = {'cycles': TickerWidget(),
                   'endgame_time': StopWatchWidget(),
                   'placement_teleop': ConeCubeWidget(),
                   'auto_start': LocationWidget()}


class PitScoutForm(forms.Form):
    template_name = 'entry/components/forms/scout.html'

    # Drivetrain
    drivetrain_style = forms.IntegerField(widget=widgets.Select(choices=[
                    (1, "foo"),
                    (2, "bar")
                ]), label='Drivetrain Style')
    drivetrain_wheels = forms.CharField(
                    widget=widgets.Textarea(attrs={'rows': 2, 'cols': 50, 'placeholder': 'Auto Notes'}),
                    label="Drivetrain Wheels",
                    required=False
                )
    drivetrain_motortype = forms.IntegerField(widget=widgets.Select(choices=[
                    (1, "foo"),
                    (2, "bar")
                ]), label='Motor Type')
    drivetrain_motorquantity = forms.IntegerField(widget=widgets.NumberInput, required=False, label='Motor Quantity')

    # Auto
    auto_route = forms.BooleanField(widget=BooleanWidget, label="Auto Route",  required=False)
    auto_description = forms.CharField(
                    widget=widgets.Textarea(attrs={'rows': 2, 'cols': 50, 'placeholder': 'Auto Notes'}),
                    label="Auto Description",
                    required=False
                )
    auto_scoring = forms.IntegerField(widget=widgets.Select(choices=[
                    (1, "foo"),
                    (2, "bar")
                ]), label='Auto Scoring')

    # Teleop
    tele_scoring = forms.IntegerField(widget=widgets.Select(choices=[
                    (1, "foo"),
                    (2, "bar")
                ]), label='Scoring')
    tele_positions = forms.IntegerField(widget=widgets.Select(choices=[
                    (1, "foo"),
                    (2, "bar")
                ]), label='Locations')
    ball_intake = forms.CharField(
                    widget=widgets.Textarea(attrs={'rows': 2, 'cols': 50, 'placeholder': 'Auto Notes'}),
                    label="Intake Description",
                    required=False
                )
    ball_capacity = forms.IntegerField(widget=TickerWidget(), initial=0, label="Ball Capacity")
    shooter_style = forms.IntegerField(widget=widgets.Select(choices=[
                    (1, "foo"),
                    (2, "bar")
                ]), label='Shooter Style')

    # Endgame
    climb_locations = forms.IntegerField(widget=widgets.Select(choices=[
                    (1, "foo"),
                    (2, "bar")
                ]), label='Climb Locations')

    # Other

    grouping("Drivetrain", [drivetrain_style, drivetrain_wheels, drivetrain_motortype, drivetrain_motorquantity])
    grouping("Autonomous", [auto_route, auto_description, auto_scoring])
    grouping("Teleoperated", [tele_scoring, tele_positions, ball_intake, ball_capacity, shooter_style])
    grouping("Endgame", [climb_locations])
    grouping("Other", [])

    class Meta:
        model = Pits()
        widgets = {'ball_capacity': TickerWidget()}


class LoginForm(forms.Form):
    template_name = 'entry/components/forms/generic.html'

    username = forms.CharField(widget=widgets.TextInput, max_length=150, validators=[UnicodeUsernameValidator()])
    password = forms.CharField(widget=widgets.PasswordInput, max_length=128)


class ImportForm(forms.Form):
    template_name = 'entry/components/forms/generic.html'

    import_type = forms.IntegerField(widget=widgets.Select(choices=[
                    # (0, "By District Key"), This is currently disabled. waiting of FIRST api
                    (1, "By Event Key"),
                    (2, "Individual Team Number"),
                    (3, "Import All"), # TODO Disable this before release
                ]), label='Import Type')
    key = forms.CharField(widget=widgets.TextInput, label="Value", min_length=2, max_length=6, required=False)

    def clean_key(self):
        if self.cleaned_data['key'] == '':
            raise ValidationError('Field cannot be empty.')
        return self.cleaned_data['key']


class SettingsForm(forms.Form):
    # TODO This will take more time, Should probably be done after Organization Redo.
    template_name = 'entry/components/forms/scout.html'

    # Tutorial
    tutorial_completed = forms.BooleanField(widget=BooleanWidget(), label='Tutorial Completed', required=False)

    # Teams Page
    images = forms.BooleanField(widget=BooleanWidget(), label='Display Robot Photos', required=False)
    filters = forms.BooleanField(widget=BooleanWidget(), label='Display Team Filters', required=False)
    district_teams = forms.BooleanField(widget=BooleanWidget(), label='Show All Teams in the District', required=False)
    teams_behaviour = forms.IntegerField(widget=widgets.Select(choices=[
                    (1, "Go to Glance (Default)"),
                    (2, "Go to Match Scouting"),
                    (3, "Go to Pit Scouting"),
                    # (4, "Go to Team Info (Coming soon)"),
                ]), label='Click/Tap Behaviour')

    # Landing Pages
    team_list_type = forms.BooleanField(widget=BooleanWidget(), label='Display Robot Photos', required=False)

