from time import sleep

from behave import *
from selenium.webdriver.common.by import By

from apps.entry.models import Schedule
from apps.entry.test.factories import ScheduleFactory

use_step_matcher("parse")


@given("lots of scheduled matches")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    event = context.organization.settings.current_event
    for i in range(0, 100):
        ScheduleFactory(event=event)

    context.browser.get(context.base_url + "/entry/schedule/")


@then("I should see a list of matches")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert len(context.browser.find_elements(By.CLASS_NAME, "scheduleTile")) > 50


@given("a scheduled {played} match")
def step_impl(context, played):
    """
    :param played: string, either "played" or "unplayed"
    :type context: behave.runner.Context
    """
    context.scheduled_match = ScheduleFactory(
        event=context.organization.settings.current_event,
        played="played" == played
    )


@when("I follow the match")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.find_element(By.ID, "match_q_" + str(context.scheduled_match.id)).click()


@then("I should see the match details")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    br = context.browser
    assert len(br.find_elements(By.CLASS_NAME, "tripleContainer")) == 2
    assert len(br.find_elements(By.CLASS_NAME, "matchDetails")) == 1
    assert len(br.find_elements(By.CLASS_NAME, "infoBox")) == 6
    assert len(br.find_elements(By.ID, "changeTeam")) == 1


@when("I am interested in the first team")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When I am interested in the first team')


@then("When I press on the first team pill")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then When I press on the first team pill')