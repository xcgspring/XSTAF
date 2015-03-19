import os
import codecs
from jinja2 import Environment, FileSystemLoader

PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(loader=FileSystemLoader(os.path.join(PATH, 'templates')))
TEMPLATE = "report.html"

class HtmlGenerator(object):
    def __init__(self, data):
        self.data = data

    @property
    def _html_content(self):
        context = {"data" : self.data}
        return TEMPLATE_ENVIRONMENT.get_template(TEMPLATE).render(context)
    
    def generate(self, output_report_location, output_report_file):
        if not os.path.isdir(output_report_location):
            os.makedirs(output_report_location)
            
        abs_output_report_file = os.path.join(output_report_location, output_report_file)
        with codecs.open(abs_output_report_file, 'w', encoding="utf_8") as f:
            f.write(self._html_content)
