from time import sleep

from behave import *
from behave_django.decorators import fixtures
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from django.contrib.auth.hashers import check_password
from django.test import Client

from apps.entry.test.factories import ScheduleFactory
from apps.organization.test.factories import EventFactory

use_step_matcher("parse")

@step("I should see the dashboard")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.browser.find_element(By.ID, 'tileContainer').is_displayed()
    assert context.browser.find_element(By.ID, 'tileContainer').is_enabled()
    assert context.browser.current_url == context.base_url + '/entry/'


@then('I should be redirected to {page}')
def step_impl(context, page):
    """
    :param page: (context.base_url + given_path) to be redirected to
    :type context: behave.runner.Context
    """
    assert context.user is not None

    WebDriverWait(context.browser, 10).until(
        expected_conditions.url_to_be(context.base_url + page)
    )
    # Check if the current URL is the expected URL
    assert context.browser.current_url == context.base_url + page


@given("I am logged in")
def step_impl(context):
    """
    This means I am logged in and authenticated properly

    :type context: behave.runner.Context
    """
    user = context.user
    assert check_password('password!', context.user.password)

    client = Client()
    client.login(username=context.user.username, password='password!')
    cookie = client.cookies['sessionid']

    # Selenium will set cookie domain based on current page domain.
    context.browser.get(context.get_url('/404-loads-fastest/'))
    context.browser.add_cookie({
        'name': 'sessionid',
        'value': cookie.value,
        'secure': False,
        'path': '/',
    })


@given("I am authenticated")
def step_impl(context):
    """
    This means I am logged in and authenticated properly

    :type context: behave.runner.Context
    """
    context.execute_steps("Given I am logged in")


@when("I access the {page_name} page")
def step_impl(context, page_name):
    """
    :param page_name: str
    :type context: behave.runner.Context
    """
    context.execute_steps(f"Given I access the {page_name} page")


@step("I access the {page_name} page")
def step_impl(context, page_name):
    """
    :param page_name: str
    :type context: behave.runner.Context
    """
    pages = {
        'login': '/organization/login/',
        'registration': '/organization/register/',
        'logout': '/organization/logout/',
        'home': '/entry/',
        'settings': '/organization/settings/',
    }
    context.browser.get(context.base_url + pages[page_name])


@when('I click the {tile_name} tile on the dashboard')
def step_impl(context, tile_name):
    """
    :param tile_name: str
    :type context: behave.runner.Context
    """
    if "tile" not in tile_name:
        tile_name = "tile" + tile_name

    context.browser.find_element(By.ID, tile_name).click()


# @fixtures('fixtures.json')
@given("We have a season")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    for i in range(10):
        ScheduleFactory(event=context.organization.settings.current_event)


@then("I should see the team details")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then I should see the team details')