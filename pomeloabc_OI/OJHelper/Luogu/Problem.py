import os, json, pyperclip
from playwright.sync_api import sync_playwright
import pomeloabc_OI.OJHelper.Luogu.Const as Const
from bs4 import BeautifulSoup
from urllib.parse import unquote
from rich.console import Console

class Problem():
    def __init__(self, user, problem_id):
        self.user = user
        self.problem_id = problem_id
        self.__code_template_conf_path = "{}/PomeloABC_OI_System_Profile/Document_Profile".format(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))

    def get(self, contest_id = None, cookie_effective_time = 86400):
        if not os.path.exists("./{}".format(self.problem_id)):
            os.mkdir("./{}".format(self.problem_id))

        old_path = os.getcwd()

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless = True)
            context = browser.new_context()

            if contest_id != None:
                os.chdir(os.path.join(old_path, ".."))

            context.add_cookies(self.user.__update_cookies__(cookie_effective_time))

            os.chdir(old_path)

            page = context.new_page()

            if contest_id != None:
                page.goto("https://www.luogu.com.cn/problem/{}?contestId={}".format(self.problem_id, contest_id))
            else:
                page.goto("https://www.luogu.com.cn/problem/{}".format(self.problem_id))

            Console().print("Now crawling problem information.")

            html = page.content()
            soup = BeautifulSoup(html, "html.parser")
            res = json.loads(unquote(soup.script.get_text().split("\"")[1]))

            problem_id = res["currentData"]["problem"]["pid"]
            problem_name = res["currentData"]["problem"]["title"]
            problem_total_submit = res["currentData"]["problem"]["totalSubmit"]
            problem_total_accepted = res["currentData"]["problem"]["totalAccepted"]
            problem_time_limit = max(res["currentData"]["problem"]["limits"]["time"])
            problem_memory_limit = max(res["currentData"]["problem"]["limits"]["memory"])
            problem_maker = res["currentData"]["problem"]["provider"]["name"]
            problem_difficulty = Const.difficulty[res["currentData"]["problem"]["difficulty"]]

            page.click("#app > div.main-container > main > div > section.main > section > div > div.action > a:nth-child(1)")

            context.grant_permissions(["clipboard-read", "clipboard-write"])
            problem_content = pyperclip.paste()

            problem_info = {
                "id": problem_id,
                "name": problem_name,
                "submission_volume": problem_total_submit,
                "throughput": problem_total_accepted,
                "time_limit": problem_time_limit,
                "memory_limit": problem_memory_limit,
                "maker": problem_maker,
                "difficulty": problem_difficulty,
            }

            Console().print("Generating the info at {}/{}/info.json".format(os.getcwd(), self.problem_id))

            with open("./{}/info.json".format(self.problem_id), "w") as file:
                json.dump(problem_info, file, indent = 4, ensure_ascii = False)

            Console().print("Generating the content at {}/{}/content.md".format(os.getcwd(), self.problem_id))

            with open("./{}/content.md".format(self.problem_id), "w") as file:
                file.write(problem_content)

            Console().print("[#52c41a]Crawling completed[/]", style = "bold")

            page.close()
            context.close()
            browser.close()

    def submit(self, code_filename, language = "C++14 (GCC 9)", o2 = True, cookie_effective_time = 86400):
        self.user.submit(self.problem_id, code_filename, language = language, o2 = o2, cookie_effective_time = cookie_effective_time)

    def generate(self, contest_id = None):
        self.get(contest_id)

        Console().print("Generating the codefile at {}/{}/{}.cpp".format(os.getcwd(), self.problem_id, self.problem_id))

        with open("{}/problem_content_conf.md".format(self.__code_template_conf_path), "r") as file:
            conf = file.read()

        with open("./{}/{}.cpp".format(self.problem_id, self.problem_id), "w") as file:
            file.write(conf)

        Console().print("[#52c41a]Generating completed[/]", style = "bold")