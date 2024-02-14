import os
import pomeloabc_OI.Generator.Utils as utils

class IO():
    def __init__(self, filename, id = None, input_suffix = ".in", output_suffix = ".out"):
        self.filename = filename
        self.id = id
        self.input_suffix = input_suffix
        self.output_suffix = output_suffix
        
        if self.id == None:
            self.id = ""
        else:
            self.id = str(self.id)
            
        self.input_filename = "{}{}{}".format(self.filename, self.id, self.input_suffix)
        self.output_filename = "{}{}{}".format(self.filename, self.id, self.output_suffix)
        
        open(self.input_filename, "w")
        open(self.output_filename, "w")
        
    def input_write(self, *args, seperator = " ", end = "\n"):
        data = utils.args_to_list(*args)
        self.input_file = open(self.input_filename, "a")
        
        for value in data[:-1]:
            self.input_file.write("{}{}".format(str(value), seperator))
        self.input_file.write("{}".format(str(data[-1])))
        self.input_file.write(end)
        
        self.input_file.close()
        
    def output_write(self, *args, seperator = " ", end = "\n"):
        data = utils.args_to_list(*args)

        self.output_file = open(self.output_filename, "a")

        for value in data[:-1]:
            self.output_file.write("{}{}".format(str(value), seperator))
        self.output_file.write("{}".format(str(data[-1])))
        self.output_file.write(end)
        
        self.output_file.close()
        
    def output_gen(self, complie_filename):
        run_expr = "./{} < {} > {}".format(complie_filename, self.input_filename, self.output_filename)

        os.system(run_expr)