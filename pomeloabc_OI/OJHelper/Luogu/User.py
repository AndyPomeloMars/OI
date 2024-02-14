import os, time, json
from playwright.sync_api import sync_playwright
import pomeloabc_OI.OJHelper.Luogu.Record as Record
from PIL import Image
from rich.console import Console

class User():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.__user_profile_conf_path = "{}/PomeloABC_OI_System_Profile/User_Profile".format(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../..")))

    def __judge_is_login__(self):
        if os.path.exists("{}/{}/luogu-cookie.json".format(self.__user_profile_conf_path, self.username)):
            return True
        else:
            return False

    def __update_cookies__(self, cookie_effective_time = 86400):
        with open("{}/{}/luogu-cookie.json".format(self.__user_profile_conf_path, self.username), "r") as file:
            cookies = json.load(file)

            for cookie in cookies:
                cookie["expires"] = time.time() + cookie_effective_time

            return cookies

    def login(self):
        with sync_playwright() as playwright:
            if not self.__judge_is_login__():
                browser = playwright.chromium.launch(headless = True)
                context = browser.new_context()
                page = context.new_page()
                page.goto("https://www.luogu.com.cn/auth/login")

                page.fill("#app > div.main-container > main > div > div > div > div > div > div > div:nth-child(1) > div > input", self.username)
                page.fill("#app > div.main-container > main > div > div > div > div > div > div > div:nth-child(2) > div > input", self.password)

                while True:
                    page.locator("#app > div.main-container > main > div > div > div > div > div > div > div:nth-child(3) > div > div.img > img").screenshot(path = "./captcha.png")
                    captcha_img = Image.open("./captcha.png")
                    captcha_img.show()
                    captcha = Console().input("Enter the captcha: ")
                    os.remove("./captcha.png")

                    page.fill("#app > div.main-container > main > div > div > div > div > div > div > div:nth-child(3) > div > div.refined-input.input-wrap.frame > input", captcha)

                    page.click("#app > div.main-container > main > div > div > div > div > div > div > button")

                    page.wait_for_timeout(1000)

                    if page.locator("body > div.swal2-container.swal2-center.swal2-fade.swal2-shown > div > div.swal2-actions > button.swal2-confirm.swal2-styled").count():
                        Console().print("[#e74c3c]Captcha error.[/]", style = "bold")
                        page.click("body > div.swal2-container.swal2-center.swal2-fade.swal2-shown > div > div.swal2-actions > button.swal2-confirm.swal2-styled")
                    else:
                        Console().print("[#52c41a]Captcha correct.[/]", style = "bold")
                        break

                page.wait_for_url("https://www.luogu.com.cn/")

                Console().print("Generating the user cookie at {}/{}/cookie.json".format(self.__user_profile_conf_path, self.username))

                if not os.path.exists("{}/{}".format(self.__user_profile_conf_path, self.username)):
                    os.mkdir("{}/{}".format(self.__user_profile_conf_path, self.username))

                with open("{}/{}/luogu-cookie.json".format(self.__user_profile_conf_path, self.username), "w") as file:
                    json.dump(context.cookies(), file, indent = 4)
                    self.cookies = context.cookies()

                Console().print("[#52c41a]Login successfully.[/]", style = "bold")

                page.close()
                context.close()
                browser.close()

    def submit(self, problem_id, code_filename, language = "C++14 (GCC 9)", o2 = True, cookie_effective_time = 86400):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless = True)
            context = browser.new_context()

            cookies = self.__update_cookies__(cookie_effective_time)
            context.add_cookies(cookies)

            page = context.new_page()

            page.goto("https://www.luogu.com.cn/problem/{}#submit".format(problem_id))

            now_language = page.text_content("#app > div.main-container > main > div > section.main > section > div > div:nth-child(2) > div.combo-wrapper.lang-select.light-black.inline > div.text.lfe-form-sz-middle").strip()
            now_o2 = page.locator(".fa-input.svg-inline--fa.fa-square").count()

            if now_language != language:
                page.click("#app > div.main-container > main > div > section.main > section > div > div:nth-child(2) > div.combo-wrapper.lang-select.light-black.inline")
                page.get_by_text("{}".format(language)).nth(1).click()

            if bool(now_o2) ==  o2:
                page.click("#app > div.main-container > main > div > section.main > section > div > div:nth-child(2) > div:nth-child(4) > label")

            with open("./{}".format(code_filename), "r") as file:
                code = file.read()
    
                page.get_by_role("textbox").nth(2).press("Meta+a")
                page.get_by_role("textbox").nth(2).fill(code)
            
            page.click("#app > div.main-container > main > div > section.main > section > div > div:nth-child(2) > button")

            Console().print("Submission completed.", style = "bold")

            page.wait_for_url("https://www.luogu.com.cn/record/**")
            page.reload()
            
            record_id = page.url[32:]

        record = Record.Record(self, record_id)
        res = record.get()

        if not os.path.exists("./{}".format(problem_id)):
            os.mkdir("./{}".format(problem_id))

        with open("./{}/R{}.json".format(problem_id, record_id), "w") as file:
            json.dump(res, file, indent = 4)
            