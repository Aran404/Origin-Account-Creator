"""
Code under GNU General Public License v3.0

Made by https://github.com/Aran404/
Made With <3 to get rid of the people who sell it (Sorry FetaaWSB and Flex <33)
"""

# General Imports
from weakref import proxy
from selenium_stealth import stealth
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from colorama import Fore, init
import os
import re
import sys
import json
import time
import random
import string
import base64
import datetime
import requests
import threading

# Initilize colorama, to not see hex code (or whatever)
init()

# Amount of accounts created in the session
Created_Accounts = 0

# Used for safe print
thread_lock = threading.Lock()


class Generator:
    def __init__(self, proxy) -> None:
        with open("config.json", "r") as config:
            self.config = json.load(config)

        self.proxy = proxy

        try:
            self.useragent = UserAgent().random
        except:
            self.useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"

    # Safe print, to not overlap when running thread tasks
    def sprint(self, message: str) -> None:
        thread_lock.acquire()
        sys.stdout.write(message)
        thread_lock.release()

    # Module made by a friend
    def get_code(self):

        timer = 0

        while timer < 5:
            timer += 1

            time.sleep(2)

            now = datetime.datetime.now()
            delta_time = now + datetime.timedelta(0, 600)
            timestamp = datetime.datetime.timestamp(delta_time)
            get_data = requests.get(
                "https://api.xitroo.com/v1/mails?locale=en&mailAddress="
                + self.email
                + "&mailsPerPage=25&minTimestamp=0&maxTimestamp="
                + str(timestamp)
            )
            if "WW91ciBFQSBTZWN1cml0eSBDb2RlIGlz" in get_data.text:
                code_0 = re.findall('"subject":"(.*?)"', get_data.text)[0]
                decode = base64.b64decode(code_0)
                return str(decode.decode("utf-8"))[-6:]

        return False

    def __init_driver__(self) -> None:
        self.sprint(f"{Fore.WHITE}[{Fore.GREEN}PROXY{Fore.WHITE}] {self.proxy}\n")

        ser = Service(f"{os.getcwd()}\chromedriver.exe")
        proxy_server = self.proxy

        if proxy_server == False:
            capabilities = None
        else:
            proxy = Proxy()
            proxy.proxy_type = ProxyType.MANUAL
            proxy.http_proxy = proxy_server
            proxy.ssl_proxy = proxy_server
            capabilities = webdriver.DesiredCapabilities.CHROME
            proxy.add_to_capabilities(capabilities)

        # Spoofing to not get detected
        options = Options()

        options.add_experimental_option(
            "excludeSwitches",
            [
                "enable-logging",
                "enable-automation",
                "ignore-certificate-errors",
                "safebrowsing-disable-download-protection",
                "safebrowsing-disable-auto-update",
                "disable-client-side-phishing-detection",
            ],
        )

        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--lang=en")
        options.add_argument("--log-level=3")
        options.add_argument("--incognito")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--profile-directory=Null")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--start-maximized")
        options.add_argument(f"--user-agent={self.useragent}")

        if bool(self.config["headless"]) is True:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")

        self.driver = webdriver.Chrome(
            service=ser, desired_capabilities=capabilities, options=options
        )

        stealth(
            self.driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

        self.driver.set_window_size(500, 570)

        self.driver.execute_cdp_cmd(
            "Network.setUserAgentOverride", {"userAgent": self.useragent}
        )

        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
            Object.defineProperty(navigator, 'deviceMemory', {
            get: () => 99
            })
        """
            },
        )

        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
                Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
                })
            """
            },
        )

        self.driver.delete_all_cookies()

    def get_dob(self):
        month = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "Decemeber",
        ]

        return {
            "year": random.randint(1970, 2000),
            "month": random.choice(month),
            "day": random.randint(1, 27),
        }

    def fill_form1(self) -> bool or str:
        try:
            self.driver.get("https://www.origin.com/can/en-us/store")

            WebDriverWait(self.driver, 40).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/div[2]/div[3]/section/div/nav/div/div[1]/div[2]",
                    )
                )
            )

            self.driver.find_element(
                By.XPATH, "/html/body/div[2]/div[3]/section/div/nav/div/div[1]/div[2]"
            ).click()

            WebDriverWait(self.driver, 40).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//a[normalize-space()='Register']")
                )
            )

            self.curent_window = self.driver.current_window_handle

            WebDriverWait(self.driver, 40).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        "origin-cta-register[type='transparent'] a:nth-child(1)",
                    )
                )
            )

            self.driver.execute_script(
                """
            document.querySelector("origin-cta-register[type='transparent'] a:nth-child(1)").click();
            """
            )

            for window in self.driver.window_handles:
                if window != self.curent_window:
                    self.login_page = window

            self.driver.close()

            self.driver.switch_to.window(self.login_page)

            self.current_url = self.driver.current_url

            WebDriverWait(self.driver, 40).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='readAccept']"))
            )

            self.driver.execute_script(
                """
            document.querySelector("label[for='readAccept']").click();
            """
            )

            month, day, year = (
                self.get_dob()["month"],
                self.get_dob()["day"],
                self.get_dob()["year"],
            )

            Select(
                self.driver.find_element(
                    By.XPATH, "//select[@id='clientreg_dobmonth-selctrl']"
                )
            ).select_by_visible_text(str(month))
            time.sleep(random.uniform(0.61, 1.231))
            Select(
                self.driver.find_element(
                    By.XPATH, "//select[@id='clientreg_dobday-selctrl']"
                )
            ).select_by_visible_text(str(day))
            time.sleep(random.uniform(0.73, 1.11))
            Select(
                self.driver.find_element(
                    By.XPATH, "//select[@id='clientreg_dobyear-selctrl']"
                )
            ).select_by_visible_text(str(year))
            time.sleep(random.uniform(0.65, 0.82))
            Select(
                self.driver.find_element(
                    By.XPATH, "//select[@id='clientreg_country-selctrl']"
                )
            ).select_by_visible_text(str(self.config["country"]))
            time.sleep(random.uniform(0.59, 1.12))

            self.sprint(
                f"{Fore.WHITE}[{Fore.GREEN}DOB{Fore.WHITE}] {month}:{day}:{year}\n"
            )
            self.sprint(
                f"{Fore.WHITE}[{Fore.GREEN}COUNTRY{Fore.WHITE}] {self.config['country']}\n"
            )

            self.driver.execute_script(
                """
            document.querySelector("#countryDobNextBtn").click()
            """
            )

            return True

        except TimeoutException:
            return "Timeout"

        except:
            return False

    def fill_form2(self) -> bool or str:
        try:
            WebDriverWait(self.driver, 40).until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='email']"))
            )

            self.email = (
                "".join(
                    random.choice(string.ascii_letters + string.digits)
                    for _ in range(8)
                )
                + "@xitroo.fr"
            )

            time.sleep(random.uniform(0.721, 1.3145))

            self.password = (
                random.choice(string.ascii_uppercase)
                + random.choice(string.ascii_lowercase)
                + random.choice(string.digits)
                + "".join(
                    random.choice(string.ascii_letters + string.digits)
                    for _ in range(10)
                )
            )
            self.username = self.config["username"] + "".join(
                random.choice(string.digits) for _ in range(5)
            )

            for char in self.email:
                time.sleep(random.uniform(0.01223, 0.0234))
                self.driver.find_element(By.CSS_SELECTOR, "#email").send_keys(char)

            time.sleep(random.uniform(0.452, 1.235))
            self.sprint(f"{Fore.WHITE}[{Fore.GREEN}EMAIL{Fore.WHITE}] {self.email}\n")

            for char in self.password:
                time.sleep(random.uniform(0.015, 0.022))
                self.driver.find_element(By.CSS_SELECTOR, "#password").send_keys(char)

            time.sleep(random.uniform(0.78, 0.9723))
            self.sprint(
                f"{Fore.WHITE}[{Fore.GREEN}PASSWORD{Fore.WHITE}] {self.password}\n"
            )

            for char in self.username:
                time.sleep(random.uniform(0.0121, 0.0245))
                self.driver.find_element(By.CSS_SELECTOR, "#originId").send_keys(char)

            time.sleep(random.uniform(0.561, 0.974))
            self.sprint(
                f"{Fore.WHITE}[{Fore.GREEN}USERNAME{Fore.WHITE}] {self.username}\n"
            )

            self.driver.execute_script(
                """
            document.querySelector("#basicInfoNextBtn").click();
            """
            )

            time.sleep(5)

            if (
                "that wasn't it" in self.driver.page_source
                and "Please solve this puzzle so we know you are a real person"
                not in self.driver.page_source
            ):

                for char in self.password:
                    time.sleep(random.uniform(0.015, 0.022))
                    self.driver.find_element(By.CSS_SELECTOR, "#password").send_keys(
                        char
                    )

                time.sleep(random.uniform(0.78, 0.9723))

                self.driver.execute_script(
                    """
                document.querySelector("#basicInfoNextBtn").click();
                """
                )

            return True

        except TimeoutException:
            return "Timeout"
        except:
            return False

    def fill_form3(self) -> bool or str:
        WebDriverWait(self.driver, 40).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.XPATH, "/html/body/div[6]/iframe")
            )
        )

        self.driver.execute_script(
            f"""
            document.querySelector("#verification-token").value = "{captcha_token}";
            document.querySelector("#FunCaptcha-Token").value = "{captcha_token}";
        """
        )

        WebDriverWait(self.driver, 40).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#submitBtn"))
        )

        self.driver.execute_script(
            """
        document.querySelector("#submitBtn").click();
        """
        )

        WebDriverWait(self.driver, 40).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#emailVerifyCode"))
        )

        self.email_verify_code = self.get_code()

        self.sprint(
            f"{Fore.WHITE}[{Fore.GREEN}EMAIL{Fore.WHITE}] Code: {self.email_verify_code}\n"
        )

        self.driver.execute_script(
            f"""
        document.querySelector("#emailVerifyCode").value = "{self.email_verify_code}";
        """
        )

        self.driver.execute_script(
            """
        document.querySelector("#btnSendCode").click();     
        """
        )

    def __main__(self) -> None:
        self.__init_driver__()  # Intilizes the driver, must have chrome binary
        form1 = self.fill_form1()

        if form1 is False:
            self.sprint(f"{Fore.WHITE}[{Fore.RED}ERROR{Fore.WHITE}] Failed at form 1\n")
            return

        elif str(form1).lower() == "Timeout":
            self.sprint(f"{Fore.WHITE}[{Fore.RED}PROXY{Fore.WHITE}] Proxy timedout\n")
            return

        form2 = self.fill_form2()

        if form2 is False:
            self.sprint(f"{Fore.WHITE}[{Fore.RED}ERROR{Fore.WHITE}] Failed at form 1\n")
            return

        elif str(form2).lower() == "Timeout":
            self.sprint(f"{Fore.WHITE}[{Fore.RED}PROXY{Fore.WHITE}] Proxy timedout\n")
            return

        form3 = self.fill_form3()

        if form3 is False:
            self.sprint(f"{Fore.WHITE}[{Fore.RED}ERROR{Fore.WHITE}] Failed at form 1\n")
            return

        elif str(form3).lower() == "Timeout":
            self.sprint(f"{Fore.WHITE}[{Fore.RED}PROXY{Fore.WHITE}] Proxy timedout\n")
            return

        with open("Accounts.txt", "a+") as accounts:
            accounts.write(f"[Email: {self.email}, Password: {self.password}]\n")

        self.sprint(
            f"{Fore.WHITE}[{Fore.GREEN}SUCCESS{Fore.WHITE}] (Email: {self.email}, Password: {self.password})\n"
        )

        global Created_Accounts

        Created_Accounts += 1

        os.system(f"title Created By Aran - Accounts Created: {Created_Accounts}")
        self.driver.quit()


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")

    proxies = open("Proxies.txt", "r").read().splitlines()

    if proxies == []:
        proxies = [None]

    os.system("title Created By Aran ")

    with open("config.json", "r") as config:
        thread_count = json.load(config)["threads"]

    while True:
        for x in range(thread_count):
            start_gen = threading.Thread(
                target=Generator(random.choice(proxies)).__main__
            )
            start_gen.start()

        for x in range(thread_count):
            start_gen.join()
