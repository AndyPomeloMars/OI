import os
import pomeloabc_OI.Utils.Differ as differ

def clap(violent_complie_filename, test_complie_filename, input_filename, violent_output_filename, test_output_filename, mode = "c", output = True):
    violent_run_expr = "./{} < {} > {}".format(violent_complie_filename, input_filename, violent_output_filename)
    test_run_expr = "./{} < {} > {}".format(test_complie_filename, input_filename, test_output_filename)

    os.system(violent_run_expr)
    os.system(test_run_expr)

    differ.diff(violent_output_filename, test_output_filename, mode, output)