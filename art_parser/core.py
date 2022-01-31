import os
import zipfile
from io import BytesIO

import requests
from pyattck import Attck
from .utils.logger import LoggingBase


class Core(metaclass=LoggingBase):

    ATOMIC_RED_TEAM_REPO = 'https://github.com/redcanaryco/atomic-red-team/zipball/master/'
    _replacement_strings = [
        '#{{{0}}}',
        '${{{0}}}'
    ]
    string_replacement_map = {
        'command_prompt': 'cmd',
        'manual': '',
        'macos': 'macOS',
        'windows': 'Windows',
        'linux': 'Linux'
    }
    tactics = [
        'Reconnaissance',
        'Resource Development',
        'Initial Access',
        'Execution',
        'Persistence',
        'Privilege Escalation',
        'Defense Evasion',
        'Credential Access',
        'Discovery',
        'Lateral Movement',
        'Collection',
        'Command and Control',
        'Exfiltration',
        'Impact'
    ]
    matrix_dict = {
        "all": [],
        "mac": [],
        "linux": [],
        "windows": []
    }
    attck = Attck(nested_subtechniques=False)

    def replace_string(self, value):
        if isinstance(value, list):
            return_string = []
            for item in value:
                if self.string_replacement_map.get(item):
                    return_string.append(self.string_replacement_map[item])
            return ','.join(return_string)
        if self.string_replacement_map.get(value):
            return self.string_replacement_map[value]
        return value

    def path_replacement(self, string, path):
        try:
            string = string.replace('$PathToAtomicsFolder', path)
        except:
            pass
        try:
            string = string.replace('PathToAtomicsFolder', path)
        except:
            pass
        return string

    def replace_command_string(self, command: str, input_arguments: list=[]):
        if command:
            if input_arguments:
                for input in input_arguments:
                    for string in self._replacement_strings:
                        try:
                            command = command.replace(str(string.format(input.name)), str(input.value))
                        except:
                            # catching errors since some inputs are actually integers but defined as strings
                            pass
        return command

    def format_strings_with_spaces(self, value):
        return value.lower().replace(' ','-')

    def create_path(self, value):
        if '.' in value:
            tech, sub = value.split('.')
            return f"{tech}/{sub}"
        return value

    def get_abs_path(self, value) -> str:
        """Formats and returns the absolute path for a path value

        Args:
            value (str): A path string in many different accepted formats

        Returns:
            str: The absolute path of the provided string
        """
        return os.path.abspath(os.path.expanduser(os.path.expandvars(value)))

    def download_atomic_red_team_repo(self, save_path, **kwargs) -> str:
        """Downloads the Atomic Red Team repository from github

        Args:
            save_path (str): The path to save the downloaded and extracted ZIP contents

        Returns:
            str: A string of the location the data was saved to.
        """
        response = requests.get(Core.ATOMIC_RED_TEAM_REPO, stream=True, **kwargs)
        z = zipfile.ZipFile(BytesIO(response.content))
        with zipfile.ZipFile(BytesIO(response.content)) as zf:
            for member in zf.infolist():
                file_path = os.path.realpath(os.path.join(save_path, member.filename))
                if file_path.startswith(os.path.realpath(save_path)):
                    zf.extract(member, save_path)
        return z.namelist()[0]
