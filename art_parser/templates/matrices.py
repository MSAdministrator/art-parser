import os
from collections import OrderedDict
from .base import Base

import attr


class Matrices(Base):

    def execute(self, matrix_dict: dict, export_path: str):
        template = self.get_template(self.atomic_matrix_template)
        matrix_dict['linux'] = self.__sort_techniques_in_order(matrix_dict['linux'])
        ordered_list = []
        ordered_dict = OrderedDict()
        for tactic in self.tactics:
            for key,val in matrix_dict['linux'].items():
                if key == tactic:
                    ordered_dict.update({
                        tactic: val
                    })
                    print(dict(ordered_dict))
                    input('press')
        with open(os.path.join(export_path, f"Matrices", f"linux" + ".md"), 'w+') as file:
            file.write(template.render({'items': dict(ordered_dict), 'title': 'Linux', 'tactics': self.tactics}))
        input('press')

        matrix_dict['windows'] = self.__sort_techniques_in_order(matrix_dict['windows'])
        matrix_dict['mac'] = self.__sort_techniques_in_order(matrix_dict['mac'])
        matrix_dict['all'] = self.__sort_techniques_in_order(matrix_dict['all'])
        template = self.get_template(self.atomic_matrix_template)
        for key,val in matrix_dict.items():
            for tactic in self.tactics:
                if tactic in val:

                    for k,v in val.items():
                        print(k, v)
                        input('press')
            print(key,val)

            input('press')
            with open(os.path.join(self.export_path, f"Matrices", f"{key}" + ".md"), 'w+') as file:
                file.write(template.render(attr.asdict(val)))

    #def
    def __sort_techniques_in_order(self, dictionary):
        return_dict = {}

        for key,val in dictionary.items():
            return_dict[key] = sorted(val, key=lambda d: list(d.keys()))
        return return_dict