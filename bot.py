# hi hello how r u?

import time
from browser import Browser
import file_manager
import random
from selenium.webdriver.common.keys import Keys


class Bot:
    browser:Browser=None
    user_data=None

    def __init__(self,user_data):
        b = Browser()
        b.startBrowser(user_data)
        self.browser=b
    
    def make_account(self):
        b=self.browser

        b.wd.get('https://quickbooks.intuit.com/choose-country/#europe')

        b.clickButtonByXpath('//*[@data-ui-object-detail="Finland"]')

        b.wd.find_elements_by_xpath(
            '//*[@data-ui-object-detail="Free 30-day trial"]')[0].click()
        
        b.wd.find_elements_by_xpath(
            '//*[@data-ui-object-detail="Free 30-day trial"]')[1].click()

        b.wd.find_element_by_xpath(
            '//*[@type="email"]').send_keys(file_manager.get_email())

        f_name, l_name = file_manager.get_f_name(), file_manager.get_l_name()
        b.wd.find_element_by_id('ius-first-name').send_keys(f_name)
        b.wd.find_element_by_id('ius-last-name').send_keys(l_name)

        b.wd.find_element_by_id(
            'ius-mobile-phone').send_keys(f'042{random.randint(1111111,9999999)}')

        b.clickButtonByID('ius-sign-up-submit-btn')

        passw = f'{chr(random.randint(65,90))}{f_name}{l_name}{random.randint(100,900)}&@'
        b.wd.find_element_by_id('ius-password').send_keys(passw)
        b.clickButtonByID('ius-sign-up-submit-btn')

        b.clickButtonByID('ius-sign-up-submit-btn')
        b.wd.find_element_by_id('ius-confirm-password').send_keys(passw)
        b.clickButtonByID('ius-sign-up-submit-btn')

        while(b.wd.current_url!='https://app.qbo.intuit.com/app/homepage?launchSetup=false'):
            time.sleep(3)

        return True
    
    def set_settigs(self):
        b=self.browser
        b.wd.get('https://app.qbo.intuit.com/app/accountsettings')
        b.waitAndGetElement('xpath','//*[@aria-label="Edit Company name"]').click()
        b.wd.find_element_by_xpath(
            '//*[@aria-label="Company name"]').send_keys(file_manager.get_company_name())
        list(filter(lambda x: x.is_displayed(),
             b.wd.find_elements_by_class_name('saveSection')))[0].click()
        b.wd.find_element_by_xpath(
            '//*[@aria-label="Edit Contact info"]').click()
        b.wd.find_element_by_xpath(
            '//*[@aria-label="Company name"]').send_keys(file_manager.get_company_name())
        b.wd.find_element_by_xpath(
            '//*[@placeholder="Email address"]').clear()
        b.wd.find_element_by_xpath(
            '//*[@placeholder="Email address"]').send_keys(file_manager.get_company_email())

        phone = b.wd.find_element_by_id('phone-form-control')
        phone.clear()
        phone.click()
        phone.clear()
        phone.send_keys(Keys.BACK_SPACE)
        phone.send_keys(Keys.BACK_SPACE)
        phone.send_keys(Keys.BACK_SPACE)
        phone.send_keys(18888888888)
        
        b.wd.find_elements_by_class_name('settingsNavItem')[2].click()

        b.wd.find_element_by_xpath('//*[@data-section="salesCommunications"]').click()

        b.wd.find_element_by_xpath('//*[@name="emailTxnText"]').clear()
        b.wd.find_element_by_xpath(
            '//*[@name="emailTxnText"]').send_keys(file_manager.get_email_message())
        list(filter(lambda x: x.is_displayed(),
            b.wd.find_elements_by_class_name('saveSection')))[0].click()
        
        b.wd.find_elements_by_class_name('settingsNavItem')[-1].click()
        b.wd.find_element_by_xpath('//*[@data-section="currency"]').click()
        b.wd.find_element_by_xpath('//*[@aria-label="Home Currency"]').send_keys('USD')

        list(filter(lambda x: x.is_displayed(),
            b.wd.find_elements_by_class_name('saveSection')))[0].click()
        
        b.wd.find_element_by_css_selector('.bottomRightButtons button').click()

        return True
    
    def send_email(self):
        b=self.browser

        b.wd.get('https://app.qbo.intuit.com/app/sales')

        b.wd.find_element_by_xpath(
            '//*[contains(text(),"Create invoice")]').find_element_by_xpath('..').click()
        
        b.clickButtonByXpath('//*[@aria-label="Close Tooltip"]', time=10)

        b.wd.find_element_by_xpath(
            '//*[@data-automation-id="input-ref-number-sales"]').clear()
        b.wd.find_element_by_xpath(
            '//*[@data-automation-id="input-ref-number-sales"]').send_keys(random.randint(999*9, 9*9*99999999))
        
        b.wd.find_element_by_xpath(
            '//*[@aria-label="Select a customer"]').send_keys(file_manager.get_f_name())
        time.sleep(2)
        b.wd.find_element_by_xpath(
            '//*[@aria-label="Select a customer"]').send_keys(Keys.ENTER)
        list(filter(lambda x: x.is_displayed(),
            b.wd.find_elements_by_xpath('//button[contains(text(),"Save")]')))[-1].click()

        email=file_manager.get_unique_email_to_send()
        b.wd.find_element_by_xpath('//*[@aria-label="Customer email"]').clear()
        b.wd.find_element_by_xpath(
            '//*[@aria-label="Customer email"]').send_keys(email)
        file_manager.set_email_done(email)

        b.clickButtonByClassName('field-amount')

        b.wd.find_element_by_xpath('//*[@aria-label="Amount"]').clear()
        b.wd.find_element_by_xpath('//*[@aria-label="Amount"]').send_keys(1122)

        b.clickButtonByClassName('field-itemId')

        b.wd.find_element_by_xpath('//*[@aria-label="ProductService"]').clear()
        b.wd.find_element_by_xpath(
            '//*[@aria-label="ProductService"]').send_keys('Services')
        b.wd.find_element_by_xpath(
            '//*[@aria-label="ProductService"]').send_keys(Keys.ENTER)

        b.wd.find_elements_by_xpath(
            '//*[@data-automation-id="button-save-combo-universal"]')[-1].click()

        time.sleep(5)

        b.wd.find_elements_by_xpath(
            '//*[@data-automation-id="button-save-combo-universal"]')[-1].click()

        b.wd.find_element_by_css_selector('.idsTSCheckbox input').click()

        b.wd.find_element_by_class_name('idsTSButton').click()

        b.wd.find_element_by_xpath('//*[@data-automation-id="batch-menu.SEND"]').click()

        b.wd.find_element_by_css_selector('input#email_to').clear()
        b.wd.find_element_by_css_selector('input#email_to').clear()
        b.wd.find_element_by_css_selector('input#email_to').send_keys(file_manager.get_email())

        b.wd.find_element_by_xpath('//*[@data-automation-id="send-button"]').click()




        















        



