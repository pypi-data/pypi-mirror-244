import json
import os
from typing import Union


class ConfigParser:
    data: dict

    def __init__(self, configuration_file: Union[str, dict]):
        if type(configuration_file) is dict:
            self.data = configuration_file
        elif os.path.exists(configuration_file):
            with open(configuration_file, "r") as jsonfile:
                self.data = json.load(jsonfile)
        else:
            try:
                self.data = json.loads(configuration_file)
            except ValueError:
                raise ValueError(f'Invalid Json file "{configuration_file}".')

    def get_configuration_proprety(self, property: str, module: str = 'common'):
        return self.data[module][property] if property in self.data[module] else None
