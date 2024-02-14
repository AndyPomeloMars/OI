import os, json

class Document():
    def __init__(self):
        self.__document_profile_conf_path = "{}/PomeloABC_OI_System_Profile/Document_Profile".format(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))

    def generate_problem_mddoc(self, markdown_filename):
        with open("{}/problem_content_conf.md".format(self.__document_profile_conf_path), "r") as file:
            conf = file.read()

        with open("./{}".format(markdown_filename), "w") as file:
            file.write(conf)

    def generate_contest_mddoc(self, markdown_filename):
        with open("{}/contest_content_conf.md".format(self.__document_profile_conf_path), "r") as file:
            conf = file.read()

        with open("./{}".format(markdown_filename), "w") as file:
            file.write(conf)

    def make_mddoc_to_pdfdoc(self, markdown_filename, pdf_filename):
        with open("{}/pandoc_conf.json".format(self.__document_profile_conf_path), "r") as file:
            conf = json.loads(file.read())

        os.system("{} {} -o {} --pdf-engine={} -H {}".format(conf["pandoc_path"], markdown_filename, pdf_filename, conf["pdf_engine"], conf["tex_conf"]))