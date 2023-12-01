import time
# import pyperclip
from selenium.webdriver import Keys
from volworld_aws_api_common.api.dom_id import dom_id

'''
@note Need explicit waits here
@ref https://stackoverflow.com/questions/68891845/selenium-python-paste-not-working-in-headless-mode
'''
# def pyperclip_copy(content):
#     pyperclip.copy(content)
#     time.sleep(0.5)


'''
@note copy & paste can NOT work in headless Jenkins tests
'''
def input_large_content_to_textarea(c, elm, content):
    # tar_id = dom_id(ids)
    print(f"content = {content}")
    print(f"elm = {elm}")
    time.sleep(1)
    # c.browser.execute_script(f"document.getElementById('{tar_id}').setAttribute('value', '{content}')");
    # c.browser.execute_script(f"document.getElementById('{tar_id}').setAttribute('value', '{content}')");
    # elm.setAttribute('value', content)
    c.browser.execute_script("arguments[0].value = arguments[1]", elm, content)
    time.sleep(1)
    elm.send_keys(Keys.ARROW_RIGHT)  # cancel selection
    elm.send_keys(Keys.SPACE)
    try:
        elm.send_keys(Keys.BACKSPACE)  # for activate JS
    except:
        print("Can NOT keyin BACKSPACE")
