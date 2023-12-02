from behave import *
from django.contrib.auth.models import User
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from django.contrib.auth.hashers import check_password
import time
use_step_matcher("re")


@step("I am on the login page")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.get(context.base_url + '/entry/login/')


@when("I submit a valid login form")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    br = context.browser
    # assert br.find_element(By.NAME, 'csrfmiddlewaretoken').is_enabled()

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
        raise AssertionError("User is not logged in")


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
    context.browser.get(context.base_url + '/entry/register/')


@then("I should see the registration form")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert 'entry/register' in str(context.browser.current_url) 
    assert context.browser.find_element(By.NAME, 'registrationForm').is_displayed()

