import csv
import os
import random
import re
import threading
import time
import traceback
import zipfile, random
from ast import arg
from inspect import Traceback

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class White_Pages_Bot:
    wd = None
    id = None
    proxyExtensionPath = None

    def __init__(self, use_proxy=False, user_agent=None, PROXY_PORT=10008) -> None:
        def __getProxyExtensionName():
            i = 0
            proxyExtensionPath = f"./extensions/proxyExtension{i}.zip"
            while os.path.exists(proxyExtensionPath):
                i += 1
                proxyExtensionPath = f"./extensions/proxyExtension{i}.zip"
            return proxyExtensionPath

        uastrings = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        ]

        options = Options()
        # options.binary_location = r'chrome\chrome.exe'
        options.add_argument("--incognito")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        options.add_argument("disable-infobars")
        options.add_argument("referer=https://www.google.com/")

        options.add_argument(f"user-agent={random.choice(uastrings)}")

        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--disable-blink-features=AutomationControlled")

        options.add_argument("--log-level=3")
        options.add_argument("--output=/dev/null")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-crash-reporter")
        options.add_argument("--disable-in-process-stack-traces")
        options.add_argument("--disable-logging")
        options.add_argument("--disable-dev-shm-usage")

        PROXY_HOST = "usa.rotating.proxyrack.net"  # rotating proxy or host
        PROXY_USER = "ashtonrooney"  # username
        PROXY_PASS = "2187bd-6a425c-b217d2-643c2f-a391d0"  # password

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
            PROXY_HOST,
            PROXY_PORT,
            PROXY_USER,
            PROXY_PASS,
        )

        path = os.path.dirname(os.path.abspath(__file__))

        if use_proxy:

            pluginfile = __getProxyExtensionName()
            self.proxyExtensionPath = pluginfile

            with zipfile.ZipFile(pluginfile, "w") as zp:
                zp.writestr("manifest.json", manifest_json)
                zp.writestr("background.js", background_js)

            options.add_extension(pluginfile)
        if user_agent:
            options.add_argument("--user-agent=%s" % user_agent)

        # self.wd = webdriver.Chrome(
        #     r"chrome\chromedriver.exe", options=options)
        self.wd = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    def get_driver(self) -> webdriver:
        return self.wd

    def __del__(self):
        if self.proxyExtensionPath:
            try:
                os.remove(self.proxyExtensionPath)
            except:
                pass

    def login(self) -> None:
        self.wd.get("https://quickbooks.intuit.com/choose-country/")
        self.wd.implicitly_wait(10)
        time.sleep(20)
        self.wd.execute_script(
            "arguments[0].click();",
            self.wd.find_element_by_xpath('//a[@title="Europe"]'),
        )
        self.wd.execute_script(
            "arguments[0].click();",
            self.wd.find_element_by_xpath('//span[normalize-space()="Finland"]'),
        )
        for i in "rashad.hasan153@gmail.com":
            self.wd.find_element_by_id("username").send_keys(i)
            time.sleep(random.uniform(0.25, 0.5))

        for i in "Qqwert12345!%$":
            self.wd.find_element_by_id("password").send_keys(i)
            time.sleep(random.uniform(0.25, 0.5))

        time.sleep(random.uniform(2, 5))

        # self.wd.find_element_by_id("password").send_keys(Keys.ENTER)
        # time.sleep(random.randint(0.05, 0.10))
        self.wd.execute_script(
            "arguments[0].click();",
            self.wd.find_element_by_xpath('//button[@type="submit"]'),
        )
        time.sleep(60)
        # self.wd.find_element_by_xpath('//button[@type="submit"]').click()
        # time.sleep(50)
        self.wd.implicitly_wait(100)

    def main(self, data):
        self.login()

        self.id = data[0]
        print("ID>", self.id)

        for i in data[1:]:
            # time.sleep(0.05)
            # print(self.id,i)
            self.wd.get("https://www.whitepages.com/phone/" + i)
            time.sleep(random.uniform(1.75, 3))
            #time.sleep(1)

            # self.wd.refresh()

            #time.sleep(3)

            self.wd.implicitly_wait(10)
            src = (
                WebDriverWait(self.wd, 10)
                .until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                .text
            )
            # print(check)
            # src = self.wd.find_elements_by_tag_name('body')[0].text

            # if not len(re.findall("No match found", src)) and not len(re.findall("\w*(?<!View )(Cell Phone)", src)) and (len(re.findall("has .+ relatives*", src)) or re.findall("This person has .+ current address and .+ previous addresses.", src) or re.findall("Properties\n[0-9]+", src) or re.findall('Map', src)):
            # if not len(re.findall("No match found", src)) and not len(re.findall("\w*(?<!View )(Cell Phone)", src)) and (len(re.findall("has .+ relatives*", src)) or re.findall("This person has .+ current address and .+ previous addresses.", src) ):
            if (
                not len(re.findall("No match found", src))
                #and not len(re.findall("\w*(?<!View )(Cell Phone)", src))
                and (
                    (len(re.findall("has .+ relatives*", src)) > 0)
                    + (
                        len(
                            re.findall(
                                "This person has .+ current address and .+ previous addresses.",
                                src,
                            )
                        )
                        > 0
                    )
                    + (len(re.findall("Properties\n[0-9]+", src)) > 0)
                    + (len(re.findall("Criminal & Traffic Records\n[0-9]+", src)) > 0)
                    + (len(re.findall("Public Records\n[0-9]+", src)) > 0)
                    + (len(re.findall("Licenses & Permits\n[0-9]+", src)) > 0)
                    + (len(re.findall("Map", src)) > 0)
                )
                >= 1
            ):

                self.save_number(i,
                len(re.findall("\w*(?<!View )(Cell Phone)", src))>0,
                not len(re.findall("\w*(?<!View )(Cell Phone)", src)),
                (
                    (len(re.findall("has .+ relatives*", src)) > 0)
                    + (
                        len(
                            re.findall(
                                "This person has .+ current address and .+ previous addresses.",
                                src,
                            )
                        )
                        > 0
                    )
                    + (len(re.findall("Properties\n[0-9]+", src)) > 0)
                    + (len(re.findall("Criminal & Traffic Records\n[0-9]+", src)) > 0)
                    + (len(re.findall("Public Records\n[0-9]+", src)) > 0)
                    + (len(re.findall("Licenses & Permits\n[0-9]+", src)) > 0)
                    + (len(re.findall("Map", src)) > 0)
                )

                )
               # print(self.id, ">    Competent>", i, sep="\t")
            # else:
                # print(self.id, ">Not Competent>", i, sep="\t")

            with open("Already_Checked.csv", "a", newline="", encoding="utf8") as f:
                writer = csv.writer(f)
                writer.writerow([i])

    def save_number(self, number,c1,c2,c):
        with open(f"./data/{self.id}.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([number,c1,c2,c])

    def run(self, data) -> threading.Thread:
        t = threading.Thread(target=self.main, args=(data,))
        return t


def get_data(saved) -> list:
    with open("quickbooks.csv", "r", encoding="utf8") as f:

        rows = [i.split(",") for i in f.readlines()]

        cols = [[j[i].strip() for j in rows if i < len(j)] for i in range(len(rows[0]))]

        names = [i[0] for i in cols]
        #print(names)
        cols = [list(set(i[1:]) - set(saved)) for i in cols]

        for i, j in enumerate(cols):
            cols[i].insert(0, names[i])

        f.close()

    return cols


if __name__ == "__main__":
    try:
        with open("Already_Checked.csv", "r", newline="", encoding="utf8") as f:
            reader = csv.reader(f)
            saved = [i[0] for i in reader]
            f.close()

        cols = get_data(saved)[:1]
        bots = []
        for port, i in enumerate(cols):
            bot = White_Pages_Bot(use_proxy=False, PROXY_PORT=10008)
            thread = bot.run(i)
            thread.start()
            bots.append(thread)

        # for i in bots:
        #     i.start()

        for i in bots:
            i.join()

    except Exception as e:
        print(traceback.format_exc())
        pass
