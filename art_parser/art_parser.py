import os
import json

from .core import Core
from .models.loader import Loader
import attr
import yaml
from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError
from jinja2 import Template
from pyattck import Attck


class ARTParser(Core):

    json_schema_path = os.path.join(
        os.path.abspath(
            os.path.dirname(__file__)
        ), 
        'data', 'jsonschema.json'
    )
    export_path = None
    atomic_red_team_path = None

    def __init__(self, export_path, atomic_red_team_path=None):
        self.export_path = export_path
        if not atomic_red_team_path:
            self.atomic_red_team_path = self.download_atomic_red_team_repo(save_path=os.getcwd())
        else:
            if os.path.exists(atomic_red_team_path) and os.path.isdir(atomic_red_team_path):
                self.atomic_red_team_path = atomic_red_team_path
        with open(self.json_schema_path, 'r') as file:
            self.json_schema = json.load(file)

    def generate(self):
        from .templates.generate import Generate
        techniques = Loader(path=self.atomic_red_team_path).load_techniques()

        max_row = 0
        for tactic in self.attck.enterprise.tactics:
            if len(tactic.techniques) > max_row:
                max_row = len(tactic.techniques)
        html = ''
        html += '<table cellpadding="0px" cellspacing="0px">'​
        # header row
        html += '<tr>' + "".join([f"<th>{tactic}</th>" for tactic in tactics]) + '</tr>'
        # data rows
        for index in range(0, max_row):
            html += '<tr>'
            for tactic in tactics:
                for _tac in attck.enterprise.tactics:
                    if tactic == _tac.name:
                        if len(_tac.techniques) > index:
                            cell_data = _tac.techniques[index].name
                        else:
                            cell_data = ''
                        html += f"<td>{cell_data}</td>"
            html += '</tr>'
        ​
        html += '</table>'

        for tactic in self.tactics:
            for tact in self.attck.enterprise.tactics:
                if tact.name == tactic:
                    print(f'Tactic: {tactic}')
                    for technique in tact.techniques:
                        print(f'Technique: {technique.name}')
                input('press')
        for tactic_name in self.tactics:
            for tactic in self.attck.enterprise.tactics:
                if tactic_name == tactic.name:
                    for technique in tactic.techniques:
                        if techniques.get(technique.id):
                            Generate(techniques[technique.id], export_path=self.export_path).execute()
                            self.matrix_dict['all'].append({
                                'tactic': tactic.name,
                                'atomic': techniques[technique.id]
                            })
                            if techniques[technique.id].platforms:
                                for platform in techniques[technique.id].platforms:
                                    self.matrix_dict[platform.lower()].append({
                                        'tactic': tactic.name,
                                        'atomic': techniques[technique.id]
                                    })
                        else:
                            for platform in technique.platforms:
                                self.matrix_dict[platform.lower()].append({
                                    'tactic': tactic.name,
                                    'atomic': None,
                                    'name': technique.name + '\n<a href="https://github.com/redcanaryco/atomic-red-team/wiki/Contributing">CONTRIBUTE A TEST</a>'
                                })
        from .templates.matrices import Matrices
        Matrices().execute(self.matrix_dict, self.export_path)


                           
        print(tactic_dict)
        input('press')
        for technique in self.attck.enterprise.techniques:
         #   for
            if techniques.get(technique.id):

                Generate(techniques[technique.id], export_path=self.export_path).execute()
                if techniques[technique.id].tactic_name not in self.matrix_dict['all']:
                    self.matrix_dict['all'][techniques[technique.id].tactic_name] = []
                self.matrix_dict['all'][techniques[technique.id].tactic_name].append({
                    'id': techniques[technique.id].attack_technique, 
                    'name': techniques[technique.id].mitre_technique_name, 
                    'url': f'https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/{techniques[technique.id].attack_technique}/{techniques[technique.id].attack_technique}.md',
                    'tactic': techniques[technique.id].tactic_name
                })
                if techniques[technique.id].platforms:
                    for platform in techniques[technique.id].platforms:
                        if platform.lower() in self.matrix_dict:
                            if techniques[technique.id].tactic_name not in self.matrix_dict[platform.lower()]:
                                self.matrix_dict[platform.lower()][techniques[technique.id].tactic_name] = []
                            self.matrix_dict[platform.lower()][techniques[technique.id].tactic_name].append({
                                'id': techniques[technique.id].attack_technique, 
                                'name': techniques[technique.id].mitre_technique_name, 
                                'url': f'https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/{techniques[technique.id].attack_technique}/{techniques[technique.id].attack_technique}.md',
                                'tactic': techniques[technique.id].tactic_name
                            })
            else:
                for platform in technique.platforms:
                    if platform.lower() in self.matrix_dict:
                        for tactic in technique.tactics:
                            if tactic.name not in self.matrix_dict[platform.lower()]:
                                self.matrix_dict[platform.lower()][tactic.name] = []
                            self.matrix_dict[platform.lower()][tactic.name].append({
                                'id': technique.id,
                                'name': technique.name + '\n<a href="https://github.com/redcanaryco/atomic-red-team/wiki/Contributing">CONTRIBUTE A TEST</a>',
                                'url': None,
                                'tactic': tactic.name
                            })
                        
        from .templates.matrices import Matrices
        Matrices().execute(self.matrix_dict, self.export_path)

    def generate_atomic_markdown_documents(self):
        with open(self.atomic_markdown_template) as file:
            template = Template(file.read())
        techniques = Loader(path=self.atomic_red_team_path).load_techniques()
        template.globals.update(self.custom_jinja2_function_dict)
        for key,val in techniques.items():
            with open(os.path.join(self.export_path, f"{key}", f"{key}" + ".md"), 'w+') as file:
                file.write(template.render(attr.asdict(val)))

    def generate_attack_matrix(self):
        all_dict = {}
        mac_dict = {}
        linux_dict = {}
        windows_dict = {}
        attck = Attck(nested_subtechniques=False)
        for tactic_name in self.tactics:
            for tactic in attck.enterprise.tactics:
                if tactic.name == tactic_name:
                    if tactic_name not in all_dict:
                        all_dict[tactic_name] = []
                    for technique in tactic.techniques:
                        all_dict[tactic_name].append({
                            technique.id: technique.name
                        })
                        if technique.platforms:
                            for platform in technique.platforms:
                                if platform.lower() == 'macos':
                                    if tactic_name not in mac_dict:
                                        mac_dict[tactic_name] = []
                                    mac_dict[tactic_name].append({
                                        technique.id: technique.name
                                    })
                                if platform.lower() == 'windows':
                                    if tactic_name not in windows_dict:
                                        windows_dict[tactic_name] = []
                                    windows_dict[tactic_name].append({
                                        technique.id: technique.name
                                    })
                                if platform.lower() == 'linux':
                                    if tactic_name not in linux_dict:
                                        linux_dict[tactic_name] = []
                                    linux_dict[tactic_name].append({
                                        technique.id: technique.name
                                    })
        linux_dict = self.__sort_techniques_in_order(linux_dict)
        windows_dict = self.__sort_techniques_in_order(windows_dict)
        mac_dict = self.__sort_techniques_in_order(mac_dict)
        all_dict = self.__sort_techniques_in_order(all_dict)
        with open(self.atomic_matrix_template) as file:
            template = Template(file.read())
        template.globals.update(self.custom_jinja2_function_dict)
        
        with open(os.path.join(self.export_path, f"Matrices", f"{key}" + ".md"), 'w+') as file:
            file.write(template.render(attr.asdict(val)))

    def __sort_techniques_in_order(self, dictionary):
        return_dict = {}
        for key,val in dictionary.items():
            return_dict[key] = sorted(val, key=lambda d: list(d.keys()))
        return return_dict

    def verify_atomic_model(self, path):
        path = self.get_abs_path(path)
        if os.path.exists(path):
            data = None
            with open(path) as f:
                data = yaml.safe_load(f)
            from .models.atomic import Atomic
            try:
                atomic = Atomic(**data)
                return True
            except TypeError as et:
                self.__logger.warning(et)
                return False
        return False

    def verify_all_against_json_schema(self):
        loader = Loader(path=self.atomic_red_team_path)
        atomics_path = loader.find_atomics(self.atomic_red_team_path)
        for atomic_entry in atomics_path:
            self.verify_json_schema(atomic_entry)
        return True

    def verify_json_schema(self, path):
        path = self.get_abs_path(path)
        if os.path.exists(path):
            data = None
            with open(path) as f:
                data = yaml.safe_load(f)
        try:
            validate(instance=data, schema=self.json_schema)
        except ValidationError as ve:
            schema_error_string = 'schema'
            for item in ve.schema_path:
                schema_error_string += f"[{item}]"
            self.__logger.error(f"Please fix atomic {path} error before continuing: {ve.message} in {schema_error_string}")
            raise ValidationError(f"Please fix atomic {path} error before continuing: {ve.message} in {schema_error_string}")
        except SchemaError as se:
            self.__logger.error(f"An error occurred validation JSON Schema: {se}")
            raise se
