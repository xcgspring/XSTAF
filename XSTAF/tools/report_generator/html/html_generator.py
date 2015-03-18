import os
from jinja2 import Environment, FileSystemLoader

PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(loader=FileSystemLoader(os.path.join(PATH, 'templates')))

class HtmlGenerator(object):
    def __init__(data):
        self.data = data

    @property
    def _html_content(self):
        context = {"data" : self.data}
        return TEMPLATE_ENVIRONMENT.get_template(self.template_file).render(context)
    
    def generate(self, output_report_location, output_report_file):
        if not os.path.isdir(output_report_location):
            os.makedirs(output_report_location)
            
        abs_output_report_file = os.path.join(output_report_location, output_report_file)
        with open(abs_output_report_file, 'w') as f:
            f.write(self._html_content)
