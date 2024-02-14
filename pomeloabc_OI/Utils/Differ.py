from rich.progress import Progress

def diff(original_filename, changed_filename, mode = "c", output = True):
    original_file, changed_file = open(original_filename), open(changed_filename)
    original_res, changed_res = original_file.readlines(), changed_file.readlines()
    diff = False

    with Progress() as progress:
        progress.console.print("[#00a7cd]Start Comparing[/]")

        task = progress.add_task("Comparing... ", total = max(len(original_res), len(changed_res)))

        for line in range(0, max(len(original_res), len(changed_res))):
            if line >= len(original_res):
                if changed_res[line].rstrip() != "":
                    if output:
                        progress.console.print("[#ff0000]>[/] Read [#d88c72]\"{}\"[/] on line {}. Expect [#d88c72]\"\"[/].".format(changed_res[line].rstrip(), line + 1))

                    diff = True
                    if mode == "f":
                        break

            elif line >= len(changed_res):
                if original_res[line].rstrip() != "":
                    if output:
                        progress.console.print("[#ff0000]>[/] Read [#d88c72]\"\"[/] on line {}. Expect [#d88c72]\"{}\"[/].".format(line + 1, original_res[line].rstrip()))

                    diff = True
                    if mode == "f":
                        break

            elif original_res[line].rstrip() != changed_res[line].rstrip():
                if output:
                    progress.console.print("[#ff0000]>[/] Read [#d88c72]\"{}\"[/] on line {}. Expect [#d88c72]\"{}\"[/].".format(changed_res[line].rstrip(), line + 1, original_res[line].rstrip()))

                diff = True
                if mode == "f":
                    break

            progress.update(task, advance = 1)

        if not diff:
            progress.console.print("[#008000]>[/] No differences found.")

        progress.console.print("[#00a7cd]Stop Comparing[/]")