import os
from jinja2 import Environment, FileSystemLoader

PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(loader=FileSystemLoader(os.path.join(PATH, 'templates')))

class HtmlGenerator(object):
    def __init__(merged_workspace):
        self.merged_workspace = merged_workspace
        self.settings = {"output_report_file" : "report.html",
                        "output_report_location" : "",
                        "report_title" : "",
                        "report_summary" : "", }

        self.template_file = "report.html"

    def apply_settings(self, **kwargs):
        for arg in kwargs.items():
            if arg[0] in self.settings:
                self.settings[arg[0]] = arg[1]

    @property
    def _html_content(self):
        context = {}
        context["report_title"] = self.settings["report_title"]
        context["report_summary"] = self.settings["report_summary"]
        context["duts"] = self.merged_workspace.duts()
        context["testsuites"] = self.merged_workspace.merged_testsuites()
        
        return TEMPLATE_ENVIRONMENT.get_template(self.template_file).render(context)
    
    def generate(self):
        output_report_file = self.settings["output_report_file"]
        output_report_location = self.settings["output_report_location"]
        if not os.path.isdir(output_report_location):
            os.makedirs(output_report_location)
            
        abs_output_report_file = os.path.join(output_report_location, output_report_file)
        with open(abs_output_report_file, 'w') as f:
            f.write(self._html_content)

