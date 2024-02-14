import json, requests
from playwright.sync_api import sync_playwright
import pomeloabc_OI.OJHelper.Luogu.Const as Const
from bs4 import BeautifulSoup
from urllib.parse import unquote
from rich.console import Console

class Record():
    def __init__(self, user, record_id):
        self.user = user
        self.record_id = record_id

    def get(self, cookie_effective_time = 86400):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless = True)
            context = browser.new_context()

            cookies = self.user.__update_cookies__(cookie_effective_time)
            context.add_cookies(cookies)

            page = context.new_page()

            page.goto("https://www.luogu.com.cn/record/{}".format(self.record_id))

            Console().print("Now crawling results.", style = "bold")

            page.screenshot(path = "a.png")

            while page.text_content("#app > div.main-container > main > div > section.side > div > div.info-rows > div:nth-child(2) > span:nth-child(2) > span").strip() in [Const.status[0], Const.status[1], ""]:
                page.wait_for_timeout(500)

            cookies_list = []
            for cookie in self.user.__update_cookies__(cookie_effective_time):
                cookies_list.append("{}={}".format(cookie["name"], cookie["value"]))

            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
                "cookie": ";".join(cookies_list)
            }

            html = requests.session().get(page.url, headers = headers)

            soup = BeautifulSoup(html.text, "html.parser")
            res = json.loads(unquote(soup.script.get_text().split("\"")[1]))

            evaluation_res = res["currentData"]["record"]["detail"]["judgeResult"]["subtasks"]

            if type(evaluation_res) == dict:
                for subtask_id in evaluation_res.keys():
                    subtask_info = evaluation_res[str(subtask_id)]

                    del subtask_info["judger"]
                    del subtask_info["__CLASS_NAME"]

                    subtask_info["test_cases"] = subtask_info.pop("testCases")

                    if type(subtask_info["test_cases"]) == dict:
                        for case_id in subtask_info["test_cases"].keys():
                            case_info = subtask_info["test_cases"][str(case_id)]

                            del case_info["signal"]
                            del case_info["exitCode"]
                            del case_info["subtaskID"]
                            del case_info["__CLASS_NAME"]
                    else:
                        for case_info in subtask_info["test_cases"]:
                            del case_info["signal"]
                            del case_info["exitCode"]
                            del case_info["subtaskID"]
                            del case_info["__CLASS_NAME"]
            else:
                for subtask_info in evaluation_res:
                    del subtask_info["judger"]
                    del subtask_info["__CLASS_NAME"]

                    subtask_info["test_cases"] = subtask_info.pop("testCases")

                    if type(subtask_info["test_cases"]) == dict:
                        for case_id in subtask_info["test_cases"].keys():
                            case_info = subtask_info["test_cases"][str(case_id)]

                            del case_info["signal"]
                            del case_info["exitCode"]
                            del case_info["subtaskID"]
                            del case_info["__CLASS_NAME"]
                    else:
                        for case_info in subtask_info["test_cases"]:
                            del case_info["signal"]
                            del case_info["exitCode"]
                            del case_info["subtaskID"]
                            del case_info["__CLASS_NAME"]

            record = {
                "record_id": res["currentTitle"],
                "compile_state_success": res["currentData"]["record"]["detail"]["compileResult"]["success"],
                "compile_result_message": res["currentData"]["record"]["detail"]["compileResult"]["message"],
                "submission_time": res["currentTime"],
                "total_time": res["currentData"]["record"]["time"],
                "total_memory": res["currentData"]["record"]["memory"],
                "status": res["currentData"]["record"]["status"],
                "score": res["currentData"]["record"]["score"],
                "result": evaluation_res
            }

            return record