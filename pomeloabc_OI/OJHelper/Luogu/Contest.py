import os, json
from playwright.sync_api import sync_playwright
import pomeloabc_OI.OJHelper.Luogu.Const as Const
import pomeloabc_OI.OJHelper.Luogu.Problem as Problem
from bs4 import BeautifulSoup
from urllib.parse import unquote
from rich.console import Console

class Contest():
    def __init__(self, user, contest_id):
        self.user = user
        self.contest_id = contest_id

    def __on_response__(self, response):
        if '/contest/scoreboard/' in response.url and response.status == 200:
            Console().print("Generating the ranklist at {}/C{}/ranklist.json".format(os.getcwd(), self.contest_id))

            res = response.json()["scoreboard"]["result"]

            for rank in res:
                for problem_id in rank["details"]:
                    problem_info = rank["details"][problem_id]
                    problem_info["time"] = problem_info.pop("runningTime")

                rank["time"] = rank.pop("runningTime")
                
                del rank["user"]["slogan"]
                del rank["user"]["badge"]
                del rank["user"]["isAdmin"]
                del rank["user"]["isBanned"]
                del rank["user"]["color"]
                del rank["user"]["ccfLevel"]
                del rank["user"]["background"]

            with open("./C{}/ranklist.json".format(self.contest_id), "w") as file:
                json.dump(res, file, indent = 4, ensure_ascii = False)
            
    def entry(self, rated = True, cookie_effective_time = 86400):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless = True)
            context = browser.new_context()
            cookies = self.user.__update_cookies__(cookie_effective_time)
            context.add_cookies(cookies)
            page = context.new_page()
            
            page.goto("https://www.luogu.com.cn/contest/{}".format(self.contest_id))

            page.click("#app > div.main-container > div.wrapper.wrapped.lfe-body.header-layout.normal > div.header > div.functional > div.operation > button")

            if rated == True:
                page.click("body > div.swal2-container.swal2-center.swal2-fade.swal2-shown > div > div.swal2-actions > button.swal2-confirm.swal2-styled")
            else:
                page.click("body > div.swal2-container.swal2-center.swal2-fade.swal2-shown > div > div.swal2-actions > button.swal2-cancel.swal2-styled")

            page.click("body > div.swal2-container.swal2-center.swal2-fade.swal2-shown > div > div.swal2-actions > button.swal2-confirm.swal2-styled")

            Console().print("[#52c41a]Entry successfully.[/]", style = "bold")

    def get(self, cookie_effective_time = 86400):
        if not os.path.exists("./C{}".format(self.contest_id)):
            os.mkdir("./C{}".format(self.contest_id))
        
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless = True)
            context = browser.new_context()
            context.add_cookies(self.user.__update_cookies__(cookie_effective_time))
            page = context.new_page()
            
            page.goto("https://www.luogu.com.cn/contest/{}".format(self.contest_id))

            Console().print("Now crawling contest information.")

            html = page.content()
            soup = BeautifulSoup(html, "html.parser")
            res = json.loads(unquote(soup.script.get_text().split("\"")[1]))

            contest_id = res["currentData"]["contest"]["id"]
            contest_name = res["currentData"]["contest"]["name"]
            contest_rule_type = Const.rule_type[res["currentData"]["contest"]["ruleType"]]
            contest_rated = res["currentData"]["contest"]["rated"]

            contest_problem_data = res["currentData"]["contestProblems"]

            for problem in contest_problem_data:
                problem["problem"]["id"] = problem["problem"].pop("pid")
                problem["problem"]["name"] = problem["problem"].pop("title")
                problem["problem"]["difficulty"] = Const.difficulty[problem["problem"].pop("difficulty")]
                
                del problem["submitted"]
                del problem["problem"]["fullScore"]
                del problem["problem"]["type"]

            contest_host = res["currentData"]["contest"]["host"]
            del contest_host["isPremium"]

            contest_start_time = res["currentData"]["contest"]["startTime"]
            contest_end_time = res["currentData"]["contest"]["endTime"]
            contest_content = res["currentData"]["contest"]["description"]

            contest_info = {
                "id": contest_id,
                "name": contest_name,
                "rule_type": contest_rule_type,
                "rated": contest_rated,
                "host": contest_host,
                "problem_info": contest_problem_data,
                "start_time": contest_start_time,
                "end_time": contest_end_time
            }

            Console().print("Generating the info at {}/C{}/info.json".format(os.getcwd(), self.contest_id))

            with open("./C{}/info.json".format(self.contest_id), "w") as file:
                json.dump(contest_info, file, indent = 4, ensure_ascii = False)

            Console().print("Generating the content at {}/C{}/content.md".format(os.getcwd(), self.contest_id))

            with open("./C{}/content.md".format(self.contest_id), "w") as file:
                file.write(contest_content)

            if page.locator("#app > div.main-container > main > div > div.card.padding-none > div > ul > li:nth-child(3) > span").count():
                page.on("response", self.__on_response__)
                page.goto("https://www.luogu.com.cn/contest/{}#scoreboard".format(self.contest_id))
                page.wait_for_load_state('networkidle')

            Console().print("[#52c41a]Crawling completed[/]", style = "bold")

            page.close()
            context.close()
            browser.close()

    def submit(self, problem_id, code_filename, language = "C++14 (GCC 9)", o2 = True, cookie_effective_time = 86400):
        self.user.submit("{}?contestId={}".format(problem_id, self.contest_id), code_filename, language = language, o2 = o2, cookie_effective_time = cookie_effective_time)

    def generate(self, cookie_effective_time = 86400):
        self.get(cookie_effective_time)

        Console().print("Reading at {}/C{}/info.json".format(os.getcwd(), self.contest_id))

        with open("./C{}/info.json".format(self.contest_id), "r") as file:
            data = json.load(file)

        old_path = os.getcwd()

        for problem in data["problem_info"]:
            os.chdir(old_path)

            problem_id = problem["problem"]["id"]

            problem = Problem.Problem(self.user, problem_id)

            os.chdir("./C{}".format(self.contest_id))

            problem.generate(self.contest_id)

        Console().print("[#52c41a]Generating completed[/]", style = "bold")