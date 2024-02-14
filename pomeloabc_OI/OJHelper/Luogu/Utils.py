import os, json, math, html2text
from playwright.sync_api import sync_playwright
import pomeloabc_OI.OJHelper.Luogu.Const as Const
from bs4 import BeautifulSoup
from urllib.parse import unquote
from rich.progress import Progress
from rich.console import Console
from rich.table import Table

def __encolor_info__(info):
    if isinstance(info, str):
        if info == "Compile Error":
            return "[#fadb14]Compile Error[/]"
        elif info == "Output Limit Exceeded":
            return "[#052242]Output Limit Exceeded[/]"
        elif info == "Memory Limit Exceeded":
            return "[#052242]Memory Limit Exceeded[/]"
        elif info == "Time Limit Exceeded":
            return "[#052242]Time Limit Exceeded[/]"
        elif info == "Wrong Answer":
            return "[#e74c3c]Wrong Answer[/]"
        elif info == "Runtime Error":
            return "[#9d3dcf]Runtime Error[/]"
        elif info == "Accepted":
            return "[#52c41a]Accepted[/]"
        elif info == "Overall Unaccepted":
            return "[#e74c3c]Overall Unaccepted[/]"
        
    elif isinstance(info, int):
        if 0 <= info < 30:
            return "[#e74c3c]{}[/]".format(str(info))
        elif 30 <= info < 60:
            return "[#f39c11]{}[/]".format(str(info))
        elif 60 <= info < 80:
            return "[#fadb14]{}[/]".format(str(info))
        else:
            return "[#52c41a]{}[/]".format(str(info))
        
    elif isinstance(info, tuple):
        if info[1] == "Gray":
            return "[#bfbfbf]{}[/]".format(str(info[0]))
        elif info[1] == "Blue":
            return "[#0e90d2]{}[/]".format(str(info[0]))
        elif info[1] == "Green":
            return "[#5eb95e]{}[/]".format(str(info[0]))
        elif info[1] == "Orange":
            return "[#e67e22]{}[/]".format(str(info[0]))
        elif info[1] == "Red":
            return "[#e74c3c]{}[/]".format(str(info[0]))
        elif info[1] == "Purple":
            return "[#8e44ad]{}[/]".format(str(info[0]))

def get_user_info(user, target_id, cookie_effective_time = 86400):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless = True)
        context = browser.new_context()
        context.add_cookies(user.__update_cookies__(cookie_effective_time))
        page = context.new_page()
        page.goto("https://www.luogu.com.cn/user/{}".format(target_id))

        Console().print("Now crawling user information.")

        html = page.content()
        soup = BeautifulSoup(html, "html.parser")
        res = json.loads(unquote(soup.script.get_text().split("\"")[1]))

        user_content = res["currentData"]["user"]["introduction"]

        Console().print("Generating the content at {}/U{}.md".format(os.getcwd(), target_id))

        with open("./U{}.md".format(target_id), "w") as file:
            file.write(user_content)

        Console().print("[#52c41a]Crawling completed[/]", style = "bold")

        page.close()
        context.close()
        browser.close()

def get_discuss_info(user, target_id, comment_count, cookie_effective_time = 86400):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless = True)
        context = browser.new_context()
        context.add_cookies(user.__update_cookies__(cookie_effective_time))
        page = context.new_page()
        page.goto("https://www.luogu.com.cn/discuss/{}?page=1".format(target_id))

        Console().print("Now crawling discussion information.")

        html = page.inner_html("#app > div.main-container > main > div > section.main > section > div.card.padding-default > div.collapsed-wrapper > div > div")
        markdown = html2text.html2text(html)

        if not os.path.exists("./D{}".format(target_id)):
            os.mkdir("./D{}".format(target_id))

        Console().print("Generating the content at {}/D{}/content.md".format(os.getcwd(), target_id, target_id))

        with open("./D{}/content.md".format(target_id, target_id), "w") as file:
            file.write(markdown)

        Console().print("[#52c41a]Generating completed[/]", style = "bold")

        Console().print("Now crawling discussion comment.")

        Console().print("Generating the comment at {}/D{}/comment.json".format(os.getcwd(), target_id, target_id))

        comment_set = {}

        page_count = math.ceil(comment_count / 10)

        comment_id = 1

        for page_id in range(1, page_count + 1):
            page.goto("https://www.luogu.com.cn/discuss/{}?page={}".format(target_id, page_id))

            html = page.content()
            soup = BeautifulSoup(html, "html.parser")
            res = json.loads(unquote(soup.script.get_text().split("\"")[1]))
            comments = res["currentData"]["replies"]["result"]

            for comment in comments:
                user_id = comment["author"]["uid"]
                user_name = comment["author"]["name"]
                comment_info = {
                    "id": user_id,
                    "name": user_name,
                    "content": comment["content"]
                }

                comment_set[str(comment_id)] = comment_info

                comment_id += 1

                if comment_id > comment_count:
                    break
            
            if comment_id > comment_count:
                break

        with open("./D{}/comment.json".format(target_id), "w") as file:
            json.dump(comment_set, file, indent = 4, ensure_ascii = False)

        Console().print("[#52c41a]Generating completed[/]", style = "bold")

        Console().print("[#52c41a]Crawling completed[/]", style = "bold")

        page.close()
        context.close()
        browser.close()

def get_message_info(user, target_id, cookie_effective_time = 86400):
    def __on_response__(response):
        """
        __on_response__(response) -> None
            intercept requests.
            parameters:
                ? response -> ?.
            examples:
                None.
        """

        if '?user={}'.format(target_id) in response.url and response.status == 200:
            Console().print("Generating the content at {}/M{}/content.json".format(os.getcwd(), target_id))

            info = {}
            message_id = 1
            res = response.json()
            messages = res["messages"]["result"]

            for message in messages:
                sender = {
                    "id": message["sender"]["uid"],
                    "name": message["sender"]["name"]
                }
                receiver = {
                    "id": message["receiver"]["uid"],
                    "name": message["receiver"]["name"]
                }
                content = message["content"]

                info[str(message_id)] = {
                        "sender": sender, 
                        "receiver": receiver, 
                        "content": content
                    }

                message_id += 1

            with open("./M{}/content.json".format(target_id), "w") as file:
                json.dump(info, file, indent = 4, ensure_ascii = False)

            Console().print("[#52c41a]Generating completed[/]", style = "bold")

    if not os.path.exists("./M{}".format(target_id)):
        os.mkdir("./M{}".format(target_id))
    
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless = True)
        context = browser.new_context()
        context.add_cookies(user.__update_cookies__(cookie_effective_time))
        page = context.new_page()

        Console().print("Now crawling message content.")

        page.on("response", __on_response__)
        page.goto("https://www.luogu.com.cn/chat")
        page.wait_for_load_state('networkidle')

        page.fill("#app > div.main-container > main > div > div.card.wrapper.padding-none > div.side > div:nth-child(2) > div > input", target_id)
        page.click("#app > div.main-container > main > div > div.card.wrapper.padding-none > div.side > div.panel-content > div > div:nth-child(1)")

        page.wait_for_timeout(1000)

        Console().print("[#52c41a]Crawling completed[/]", style = "bold")

        page.close()
        context.close()
        browser.close()

def print_evaluation_res(data):
    compile_state_success = data["compile_state_success"]
    compile_result_message = data["compile_result_message"]
    evaluation_res = data["result"]

    table = Table(show_lines = True)
    table.add_column("TestPoints")
    table.add_column("State")
    table.add_column("Score")
    table.add_column("Time")
    table.add_column("Memory")
    table.add_column("Description")

    with Progress() as progress:
        progress.console.print("Solution submitted with record ID {}.".format(str(data["record_id"])))

        if compile_state_success != True:
            progress.console.print("{}:\n{}".format(__encolor_info__("Compile Error"), compile_result_message))
            return

        if type(evaluation_res) == dict:
            for subtask_id in evaluation_res.keys():
                subtask_info = evaluation_res[str(subtask_id)]
                subtask_id = subtask_info["id"]
                subtask_status = subtask_info["status"]
                subtask_score = subtask_info["score"]
                subtask_time = subtask_info["time"]
                subtask_memory = subtask_info["memory"]

                table.add_row("Subtask {}".format(str(subtask_id)), __encolor_info__(Const.status[subtask_status]), "{} pts".format(__encolor_info__(subtask_score)), "{} ms".format(str(subtask_time)), "{} KB".format(str(subtask_memory)), "\\")

                if type(subtask_info["test_cases"]) == dict:
                    for case_id in subtask_info["test_cases"].keys():
                        case_info = subtask_info["test_cases"][str(case_id)]
                        case_id = case_info["id"]
                        case_status = case_info["status"]
                        case_score = case_info["score"]
                        case_time = case_info["time"]
                        case_memory = case_info["memory"]
                        case_description = case_info["description"]

                        table.add_row("      # {}".format(str(case_id)), __encolor_info__(Const.status[case_status]), "{} pts".format(__encolor_info__(case_score)), "{} ms".format(str(case_time)), "{} KB".format(str(case_memory)), "None" if case_description == "" else case_description)
                
                else:
                    for case_info in subtask_info["test_cases"]:
                        case_id = case_info["id"]
                        case_status = case_info["status"]
                        case_score = case_info["score"]
                        case_time = case_info["time"]
                        case_memory = case_info["memory"]
                        case_description = case_info["description"]

                        table.add_row("      # {}".format(str(case_id)), __encolor_info__(Const.status[case_status]), "{} pts".format(__encolor_info__(case_score)), "{} ms".format(str(case_time)), "{} KB".format(str(case_memory)), "None" if case_description == "" else case_description)

        else:
            for subtask_info in evaluation_res:
                subtask_id = subtask_info["id"]
                subtask_status = subtask_info["status"]
                subtask_score = subtask_info["score"]
                subtask_time = subtask_info["time"]
                subtask_memory = subtask_info["memory"]

                table.add_row("Subtask {}".format(str(subtask_id)), __encolor_info__(Const.status[subtask_status]), "{} pts".format(__encolor_info__(subtask_score)), "{} ms".format(str(subtask_time)), "{} KB".format(str(subtask_memory)), "\\")

                if type(subtask_info["test_cases"]) == dict:
                    for case_id in subtask_info["test_cases"].keys():
                        case_info = subtask_info["test_cases"][str(case_id)]
                        case_id = case_info["id"]
                        case_status = case_info["status"]
                        case_score = case_info["score"]
                        case_time = case_info["time"]
                        case_memory = case_info["memory"]
                        case_description = case_info["description"]

                        table.add_row("      # {}".format(str(case_id)), __encolor_info__(Const.status[case_status]), "{} pts".format(__encolor_info__(case_score)), "{} ms".format(str(case_time)), "{} KB".format(str(case_memory)), "None" if case_description == "" else case_description)
                
                else:
                    for case_info in subtask_info["test_cases"]:
                        case_id = case_info["id"]
                        case_status = case_info["status"]
                        case_score = case_info["score"]
                        case_time = case_info["time"]
                        case_memory = case_info["memory"]
                        case_description = case_info["description"]

                        table.add_row("      # {}".format(str(case_id)), __encolor_info__(Const.status[case_status]), "{} pts".format(__encolor_info__(case_score)), "{} ms".format(str(case_time)), "{} KB".format(str(case_memory)), "None" if case_description == "" else case_description)

        table.add_row("Total", __encolor_info__(Const.status[data["status"]]), "{} pts".format(__encolor_info__(data["score"])), "{} ms".format(data["total_time"]), "{} KB".format(data["total_memory"]), "\\")

        progress.console.print(table)

def print_ranklist(path):
    with open(path, "r") as file:
        res = json.loads(file.read())

    with Progress() as progress:
        table = Table(show_lines = True)
        table.add_column("Rank")
        table.add_column("User")
        table.add_column("TotalScore")

        column_beadd = False
        column_name = "A"
        row_rank = 1

        for user in res:
            username = user["user"]["name"]
            total_score = user["score"]
            total_runningtime = user["time"]

            problem_details = user["details"]
            problem_info = []

            for problem_id in problem_details.keys():
                if not column_beadd:
                    table.add_column(column_name)
                    column_name = chr(ord(column_name) + 1)

                problem_score = problem_details[problem_id]["score"]
                problem_runningtime = problem_details[problem_id]["time"]

                problem_info.append("{} pts\n{} ms".format(__encolor_info__(problem_score), problem_runningtime))

            column_beadd = True

            table.add_row("#{}".format(str(row_rank)), username, "{} pts\n{} ms".format(__encolor_info__(total_score), total_runningtime), *problem_info)

            row_rank += 1

        progress.console.print(table)