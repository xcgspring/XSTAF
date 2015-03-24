import os
import shutil

class CSVGenerator(object):
    def __init__(self, data):
        self.data = data
    
    def generate(self, output_report_location):
        if os.path.isdir(output_report_location):
            shutil.rmtree(output_report_location)
        os.makedirs(output_report_location)
        
        for testsuite in self.data.testsuites:
            abs_output_report_file = os.path.join(output_report_location, testsuite.name+".csv")
            with open(abs_output_report_file, 'w') as f:
                for testcase in testsuite.testcases:
                    f.write("%s,%s,%s\n" % (testcase.name, testcase.result, testcase.description))
