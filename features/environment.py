from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from apps.organizations.test.factories import OrgMemberFactory


def before_all(context):
    context.browser = webdriver.Chrome()
    context.browser.implicitly_wait(1)
    # context.wait = WebDriverWait(context.browser, 3)


def after_all(context):
    # Explicitly quits the browser, otherwise it won't once tests are done
    context.browser.quit()


def before_scenario(context, scenario):
    context.org_member = OrgMemberFactory()
    context.user = context.org_member.user
