# hi hello how r u?

import time
from browser import Browser
import file_manager
import random
from selenium.webdriver.common.keys import Keys


class Bot:
    browser: Browser = None
    user_data = None

    def __init__(self, user_data="D:/Script- Baackup/quickbook/Chrome/User Data"):
        b = Browser()
        b.startBrowser(user_data=r"%s" % (user_data))
        self.browser = b

    def make_account(self):
        b = self.browser

        b.wd.get('https://quickbooks.intuit.com/choose-country/#europe')

        b.clickButtonByXpath('//*[@data-ui-object-detail="Finland"]')

        b.executeScript(
            'window.scrollTo(document.documentElement.scrollTop,document.documentElement.scrollTop+200);')

        time.sleep(1)
        b.wd.find_elements_by_xpath(
            '//*[@data-ui-object-detail="Free 30-day trial"]')[0].click()

        time.sleep(1)
        b.executeScript(
            'window.scrollTo(document.documentElement.scrollTop,document.documentElement.scrollTop+200);')
        time.sleep(1)

        b.wd.find_elements_by_xpath(
            '//*[@data-ui-object-detail="Free 30-day trial"]')[1].click()

        b.waitAndGetElement('xpath',
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

        time.sleep(30)

        b.wd.get('https://app.qbo.intuit.com/app/homepage?launchSetup=false')

        # while(b.wd.current_url != 'https://app.qbo.intuit.com/app/homepage?launchSetup=false'):
        #     time.sleep(3)

        return True

    def set_settings(self):
        b = self.browser
        b.wd.get('https://app.qbo.intuit.com/app/accountsettings')
        b.waitAndGetElement(
            'xpath', '//*[@aria-label="Edit Company name"]',time=20).click()
        b.wd.find_element_by_xpath(
            '//*[@aria-label="Company name"]').send_keys(file_manager.get_company_name())
        list(filter(lambda x: x.is_displayed(),
             b.wd.find_elements_by_class_name('saveSection')))[0].click()
        time.sleep(2)

        b.waitAndGetElement('xpath',
                            '//*[@aria-label="Edit Contact info"]').click()

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

        list(filter(lambda x: x.is_displayed(),
             b.wd.find_elements_by_class_name('saveSection')))[0].click()
        time.sleep(2)

        b.wd.find_elements_by_class_name('settingsNavItem')[2].click()

        b.waitAndGetElement('xpath',
                            '//*[@data-section="salesCommunications"]').click()

        b.wd.find_element_by_xpath('//*[@name="emailTxnText"]').clear()
        b.wd.find_element_by_xpath(
            '//*[@name="emailTxnText"]').send_keys(file_manager.get_email_message())
        list(filter(lambda x: x.is_displayed(),
                    b.wd.find_elements_by_class_name('saveSection')))[0].click()
        time.sleep(2)

        b.wd.find_elements_by_class_name('settingsNavItem')[-1].click()
        b.waitAndGetElement('xpath', '//*[@data-section="currency"]').click()
        b.wd.find_element_by_xpath(
            '//*[@aria-label="Home Currency"]').send_keys('USD')

        list(filter(lambda x: x.is_displayed(),
                    b.wd.find_elements_by_class_name('saveSection')))[0].click()
        time.sleep(2)

        b.wd.find_element_by_css_selector('.bottomRightButtons button').click()

        return True

    def send_email(self):
        b = self.browser

        b.wd.get('https://app.qbo.intuit.com/app/sales')

        # b.wd.find_element_by_xpath(
        #     '//*[contains(text(),"Create invoice")]').find_element_by_xpath('..').click()

        # b.clickButtonByXpath('//*[@aria-label="Close Tooltip"]', time=20)

        # b.wd.find_element_by_xpath(
        #     '//*[@data-automation-id="input-ref-number-sales"]').clear()
        # b.wd.find_element_by_xpath(
        #     '//*[@data-automation-id="input-ref-number-sales"]').send_keys(random.randint(999*1, 9*999))

        # b.wd.find_element_by_xpath(
        #     '//*[@aria-label="Select a customer"]').send_keys(file_manager.get_f_name())
        # time.sleep(3)
        # b.wd.find_element_by_xpath(
        #     '//*[@aria-label="Select a customer"]').send_keys(Keys.ENTER)
        # time.sleep(3)
        # list(filter(lambda x: x.is_displayed(),
        #             b.wd.find_elements_by_xpath('//button[contains(text(),"Save")]')))[-1].click()

        # time.sleep(7)

        # email = file_manager.get_unique_email_to_send()
        # b.wd.find_element_by_xpath('//*[@aria-label="Customer email"]').clear()
        # b.wd.find_element_by_xpath(
        #     '//*[@aria-label="Customer email"]').send_keys(email)
        # file_manager.set_email_done(email)

        # b.clickButtonByClassName('field-amount')

        # b.wd.find_element_by_xpath('//*[@aria-label="Amount"]').clear()
        # b.wd.find_element_by_xpath('//*[@aria-label="Amount"]').send_keys(1122)

        # b.clickButtonByClassName('field-itemId')

        # b.wd.find_element_by_xpath('//*[@aria-label="ProductService"]').clear()
        # b.wd.find_element_by_xpath(
        #     '//*[@aria-label="ProductService"]').send_keys('Services')
        # b.wd.find_element_by_xpath(
        #     '//*[@aria-label="ProductService"]').send_keys(Keys.ENTER)

        # b.wd.find_elements_by_xpath(
        #     '//*[@data-automation-id="button-save-combo-universal"]')[-1].click()

        # time.sleep(10)

        # b.wd.find_elements_by_xpath(
        #     '//*[@data-automation-id="button-save-combo-universal"]')[-1].click()

        b.waitAndGetElement('css', '.idsTSCheckbox input').click()

        for i in range(25):    
            print(i)
            b.waitAndGetElement('class','idsTSButton').click()

            b.waitAndGetElement('xpath',
                '//*[@data-automation-id="batch-menu.SEND"]').click()

            time.sleep(5)
            b.waitAndGetElement('css', 'input#email_to').clear()
            b.wd.find_element_by_css_selector('input#email_to').clear()

            email=file_manager.get_email()

            b.wd.find_element_by_css_selector(
                'input#email_to').send_keys(email)

            file_manager.set_email_done(email)

            b.wd.find_element_by_xpath(
                '//*[@data-automation-id="send-button"]').click()
            time.sleep(5)
            



if __name__ == '__main__':
    b = Bot(r"D:\Script- Baackup\quickbook\Chrome\User Data")
    b.make_account()
    b.set_settings()
    b.send_email()
