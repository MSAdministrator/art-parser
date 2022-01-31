import os
from ..core import Core

from jinja2 import Template
from pyattck import Attck


class Base(Core):

    atomic_markdown_template = os.path.join(
        os.path.abspath(
            os.path.dirname(os.path.dirname(__file__))
        ), 
        'data', 
        'atomic_doc.jinja2'
    )
    atomic_matrix_template = os.path.join(
        os.path.abspath(
            os.path.dirname(os.path.dirname(__file__))
        ), 
        'data', 
        'matrix.jinja2'
    )

    def __init__(self):
        self.custom_jinja2_function_dict = {
            "path_replacement": self.path_replacement,
            "replace_command_string": self.replace_command_string,
            "format_strings_with_spaces": self.format_strings_with_spaces,
            "replace_string": self.replace_string,
            "create_path": self.create_path
        }

    def get_template(self, value):
        with open(value) as file:
            template = Template(file.read())
        template.globals.update(self.custom_jinja2_function_dict)
        return template

    def get_tactic(self, attack_technique):
        for technique in self.attck.enterprise.techniques:
            if technique.id == attack_technique:
                for tactic in technique.tactics:
                    return tactic.name, tactic.id

    def get_platforms(self, attack_technique):
        for technique in self.attck.enterprise.techniques:
            if technique.id == attack_technique:
                if technique.platforms:
                    return technique.platforms

    def get_technique_name(self, attack_technique):
        for technique in self.attck.enterprise.techniques:
            if technique.id == attack_technique:
                return technique.name
