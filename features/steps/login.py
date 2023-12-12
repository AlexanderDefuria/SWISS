from time import sleep

from behave import *
from django.contrib.auth.models import User
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from apps.common.tests.faker import faker
from features.helpers import click_button

use_step_matcher("re")


@step("I am on the login page")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.get(context.base_url + '/organization/login/')


@when("I submit a valid login form")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    br = context.browser

    # Fill login form and submit it (valid version)
    assert len(User.objects.all()) >= 1
    br.find_element(By.NAME, 'username').send_keys(context.user.username)
    br.find_element(By.NAME, 'password').send_keys('password!')
    br.find_element(By.NAME, 'loginButton').click()

@when("I am logged in")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    print(User.objects.all())
    context.execute_steps(u"""
        Given I am anonymous
        And I am on the login page
        When I submit a valid login form
    """)


@step("I am anonymous")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.delete_cookie('sessionid')
    context.browser.refresh()


@then("I should be logged in")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    try:
        assert context.browser.find_element(By.ID, 'sidebarUserNameDisplay').is_enabled()
    except NoSuchElementException:
        raise AssertionError("User is not logged in: We can't see the sidebarUserNameDisplay element")


@when("I submit an invalid login form")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    br = context.browser

    # Fill login form and submit it (invalid version)
    br.find_element(By.NAME, 'username').send_keys('user_that_dne')
    br.find_element(By.NAME, 'password').send_keys('silly.silly.non.password')
    br.find_element(By.NAME, 'loginButton').click()


@then("I should see the login form")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.browser.find_element(By.NAME, 'loginForm').is_displayed()


@step("I should see an error message")
def step_impl(context):
    """
    TODO: Implement error message
    :type context: behave.runner.Context
    """
    pass


@when("I access the registration page")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.get(context.base_url + '/organization/register/')


@then("I should see the registration form")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert 'organization/register' in str(context.browser.current_url)
    assert context.browser.find_element(By.NAME, 'registrationForm').is_displayed()


@when("I submit a valid registration form")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    br = context.browser
    password = faker.password()
    email = faker.email()

    # Fill registration form and submit it (valid version)
    br.find_element(By.NAME, 'username').send_keys(faker.user_name())
    br.find_element(By.NAME, 'password').send_keys(password)
    br.find_element(By.NAME, 'password_validate').send_keys(password)
    br.find_element(By.NAME, 'first_name').send_keys(faker.first_name())
    br.find_element(By.NAME, 'last_name').send_keys(faker.last_name())
    br.find_element(By.NAME, 'email').send_keys(email)
    br.find_element(By.NAME, 'email_validate').send_keys(email)
    br.find_element(By.NAME, 'submit').click()


@when("I add a new organization's details")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    br = context.browser

    # Fill registration form and submit it (valid version)
    br.find_element(By.ID, 'id_org_name').send_keys(faker.user_name())
    click_button(context, 'create_new_org_true')


@when("I add an existing organization's details")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    br = context.browser

    # Fill registration form and submit it (valid version)
    click_button(context, 'create_new_org_false')
    br.find_element(By.ID, 'id_org_name').send_keys('user_that_dne')
    br.find_element(By.ID, 'id_org_reg_id').send_keys('user_that_dne')
