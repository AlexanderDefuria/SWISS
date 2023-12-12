from selenium.webdriver.common.by import By


def click_button(context, button_name, button_id=None):
    """
    :type context: behave.runner.Context
    :type button_name: str
    :type button_id: str | None
    """
    if id:
        element = context.browser.find_element(By.ID, button_name)
    else:
        element = context.browser.find_element(By.NAME, button_name)
    context.browser.execute_script("arguments[0].click();", element)
