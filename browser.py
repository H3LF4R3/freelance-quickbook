import os
import random
import traceback
import warnings
import zipfile
from ast import literal_eval
from distutils.log import warn
from time import sleep

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

warnings.filterwarnings("ignore")


class Browser:

    Chrome_UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"

    def __init__(self):
        self.userDataDirPath = None
        self.profileName = None
        self.wd = None
        self.simpleProxy = None
        self.proxyExtensionPath = ""
        self.packedExtension = list()

    def startBrowser(
        self,
        path="",
        url="",
        userAgent="",
        setMaximizeWindow=True,
        headless=False,
        is_Chrome_Driver_Manager=True,
        user_data=''
    ):
        if self.proxyExtensionPath:
            self.packedExtension.append(self.proxyExtensionPath)
        options = self.__getArguments(userAgent, headless, user_data)
        if is_Chrome_Driver_Manager:
            self.wd = webdriver.Chrome(
                ChromeDriverManager().install(), options=options)

        self.wd.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
            Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
            })
        """
            },
        )
        if setMaximizeWindow == True:
            self.maximizeWindow()
        if isinstance(url, str) and url:
            self.getPage(url)

    def init_incogniton(self, _id):
        incogniton_url = "http://127.0.0.1:35000/automation/launch/python/" + _id
        resp = requests.get(
            url=incogniton_url,
            headers={"User-Agent": self.Chrome_UserAgent},
            timeout=15000,
        )

        incomingJson = resp.json()
        self.wd = webdriver.Remote(
            command_executor=incomingJson["url"],
            desired_capabilities=literal_eval(incomingJson["dataDict"]),
            options=self.__getArguments(self.Chrome_UserAgent, headless=False),
        )

        self.wd.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
            Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
            })
        """
            },
        )

    def getPage(self, url):
        self.wd.get(url)

    def maximizeWindow(self):
        self.wd.maximize_window()

    def getOpenedTabsCount(self) -> int:
        return len(self.wd.window_handles)

    def closeTabeByIndex(self, index):
        self.switchTab(index)
        self.wd.close()

    def switchTab(self, tabNum):
        self.wd.switch_to.window(self.wd.window_handles[tabNum])

    def addPackedExtension(self, packedExtensions):
        """
        Add packed extension to the browser.Extension must be packed i.e .crx files and in the same folder

        Args:
            nameExtensions (list): List containing name of the packed extension
        """
        self.packedExtension = packedExtensions

    def sendKeysByName(self, name, key) -> bool():
        try:
            WebDriverWait(self.wd, 20).until(
                EC.element_located_to_be_selected((By.NAME, name))
            ).send_keys(key)
            # self.wd.find_element(())
            return True
        except:
            return False

    def sendKeysByXpath(self, xpath, key) -> bool():
        try:
            self.wd.find_element((By.XPATH, xpath)).send_keys(key)
            return True
        except:
            return False

    def sendKeysByID(self, id, key) -> bool():
        try:
            self.wd.find_element((By.ID, id)).send_keys(key)
            return True
        except:
            return False

    def isClickableElementFoundByXpath(self, xpath, time):
        return WebDriverWait(self.wd, time).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )

    def clickButtonByName(self, name, time=10) -> bool():
        try:
            element = WebDriverWait(self.wd, time).until(
                EC.element_to_be_clickable((By.NAME, name))
            )
            element.click()
            return True
        except:
            pass
        return False

    def clickButtonByXpath(self, xpath, time=10) -> bool():
        try:
            element = self.isClickableElementFoundByXpath(xpath, time)
            element.click()
            return True
        except:
            return False

    def clickButtonByID(self, id, time=10) -> bool():
        try:
            element = WebDriverWait(self.wd, time).until(
                EC.element_to_be_clickable((By.ID, id))
            )
            element.click()
            return True
        except Exception as exc:
            return False

    def clickButtonByClassName(self, className, time=10) -> bool():
        try:
            element = WebDriverWait(self.wd, time).until(
                EC.element_to_be_clickable((By.CLASS_NAME, className))
            )
            element.click()
            return True
        except:
            return False

    def getElementByClassName(self, className, time=10):
        try:
            element = WebDriverWait(self.wd, time).until(
                EC.presence_of_element_located((By.CLASS_NAME, className))
            )
            return element
        except:
            return None

    def waitAndGetElement(self, type, element, time=10):
        try:
            if type == "id":
                type = By.ID
            elif type == "class":
                type = By.CLASS_NAME
            elif type == "xpath":
                type = By.XPATH
            elif type == "css":
                type = By.CSS_SELECTOR

            return WebDriverWait(self.wd, time).until(
                EC.presence_of_element_located((type, element))
            )
        except:
            return None

    def executeScript(self, script):
        self.wd.execute_script(script)

    def clickElementByJS(self, element):
        self.wd.execute_script("arguments[0].click();", element)

    def openNewTab(self, url=""):
        self.wd.execute_script(f"""window.open("{url}","_blank");""")

    def addProfile(self, userDataDirPath, profileName):
        self.userDataDirPath = userDataDirPath
        self.profileName = profileName

    def __getArguments(self, userAgent="", headless=False, user_data='', ):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-crash-reporter")
        options.add_argument("--disable-in-process-stack-traces")
        options.add_argument("--disable-logging")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--log-level=3")
        options.add_argument("--output=/dev/null")

        if user_data:
            # e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
            options.add_argument(r"--user-data-dir="+user_data)
            options.add_argument(
                '--profile-directory=Profile 2')  # e.g. Profile 3

        options.add_experimental_option(
            "prefs", {"profile.default_content_setting_values.notifications": 2}
        )

        # Argument for english language
        options.add_argument("--lang=en-ca")
        # Remove automation header
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])

        # Adding profile
        if self.profileName:
            options.add_argument(
                "user-data-dir={0}".format(self.userDataDirPath))
            options.add_argument(
                "profile-directory={0}".format(self.profileName))
        if self.simpleProxy:
            options.add_argument("--proxy-server=%s" % self.simpleProxy)
        if isinstance(userAgent, str) and isinstance:
            options.add_argument(f"user-agent={userAgent}")
        if headless == True:
            options.add_argument("--headless")
        if len(self.packedExtension) > 0:
            for packedExtension in self.packedExtension:
                options.add_extension(packedExtension)

        # # Argument to disbale popup of password save
        # prefs = {"credentials_enable_service":False,"profile.password_manager_enabled":False,"profile.default_content_setting_values.notifications" : 2}
        # prefs = {"credentials_enable_service": False,
        #  "profile.password_manager_enabled": False}
        # options.add_experimental_option("prefs", prefs)
        return options

    def element_completely_viewable(self, elem) -> bool:

        elem_left_bound = elem.location.get("x")
        elem_top_bound = elem.location.get("y")
        elem_width = elem.size.get("width")
        elem_height = elem.size.get("height")
        elem_right_bound = elem_left_bound + elem_width
        elem_lower_bound = elem_top_bound + elem_height

        win_upper_bound = self.wd.execute_script("return window.pageYOffset")
        win_left_bound = self.wd.execute_script("return window.pageXOffset")
        win_width = self.wd.execute_script(
            "return document.documentElement.clientWidth"
        )
        win_height = self.wd.execute_script(
            "return document.documentElement.clientHeight"
        )
        win_right_bound = win_left_bound + win_width
        win_lower_bound = win_upper_bound + win_height

        return all(
            (
                win_left_bound <= elem_left_bound,
                win_right_bound >= elem_right_bound,
                win_upper_bound <= elem_top_bound,
                win_lower_bound >= elem_lower_bound,
            )
        )

    def scroll_to_element(self, elem, key="page"):
        elem_left_bound = elem.location.get("x")
        elem_top_bound = elem.location.get("y")
        elem_width = elem.size.get("width")
        elem_height = elem.size.get("height")
        elem_right_bound = elem_left_bound + elem_width
        elem_lower_bound = elem_top_bound + elem_height

        win_upper_bound = self.wd.execute_script("return window.pageYOffset")
        win_left_bound = self.wd.execute_script("return window.pageXOffset")
        win_width = self.wd.execute_script(
            "return document.documentElement.clientWidth"
        )
        win_height = self.wd.execute_script(
            "return document.documentElement.clientHeight"
        )
        win_right_bound = win_left_bound + win_width
        win_lower_bound = win_upper_bound + win_height

        top, bottom = (
            win_upper_bound <= elem_top_bound,
            win_lower_bound >= elem_lower_bound,
        )

        body = self.wd.find_element_by_tag_name("body")
        # print(top,bottom)
        count = 10
        while not self.element_completely_viewable(elem) and count:
            count -= 1

            sleep(random.uniform(0.05, 0.25))

            if not top:
                # print('t')
                if key == "page":
                    body.send_keys(Keys.PAGE_UP)
                    body.send_keys(Keys.PAGE_UP)
                else:
                    body.send_keys(Keys.UP)
                    body.send_keys(Keys.UP)
            elif not bottom:
                # print('b')
                if key == "page":
                    body.send_keys(Keys.PAGE_DOWN)
                    body.send_keys(Keys.PAGE_DOWN)
                else:
                    body.send_keys(Keys.DOWN)
                    body.send_keys(Keys.DOWN)

        ActionChains(self.wd).move_to_element(elem).perform()

        desired_y = (elem.size["height"] / 2) + elem.location["y"]
        window_h = self.wd.execute_script("return window.innerHeight")
        window_y = self.wd.execute_script("return window.pageYOffset")
        current_y = (window_h / 2) + window_y
        scroll_y_by = desired_y - current_y

        self.wd.execute_script(
            "window.scrollBy(0, arguments[0]);", scroll_y_by)
        # elem.location_once_scrolled_into_view

        return elem

    def addSimpleProxy(self, proxy):
        self.simpleProxy = proxy

    def addAuthenticateProxy(self, proxyHost, proxyPort, proxyUser, proxyPassword):
        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                  singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                  },
                  bypassList: ["localhost"]
                }
              };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (
            proxyHost,
            proxyPort,
            proxyUser,
            proxyPassword,
        )
        pluginfile = self.__getProxyExtensionName()
        self.proxyExtensionPath = pluginfile
        with zipfile.ZipFile(pluginfile, "w") as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)

    def __getProxyExtensionName(self):
        i = 0
        proxyExtensionPath = f"proxyExtension{i}.zip"
        while os.path.exists(proxyExtensionPath):
            i += 1
            proxyExtensionPath = f"proxyExtension{i}.zip"
        return proxyExtensionPath

    def __del__(self):
        if self.proxyExtensionPath:
            try:
                os.remove(self.proxyExtensionPath)
            except:
                pass


if __name__ == "__main__":
    browser = Browser()
    browser.startBrowser(
        user_data=r"D:\Script- Baackup\quickbook\Chrome\User Data")
