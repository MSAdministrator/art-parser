import os

from ..models.atomic import Atomic
from .base import Base
from .matrices import Matrices

import attr
from jinja2 import Template


class Generate(Base):

    def __init__(self, atomic: Atomic, export_path: str):
        super().__init__()
        self.atomic = atomic
        self.atomic.mitre_technique_name = self.get_technique_name(self.atomic.attack_technique)
        self.atomic.tactic_name, self.atomic.tactic_id = self.get_tactic(self.atomic.attack_technique)
        self.atomic.platforms = self.get_platforms(self.atomic.attack_technique)
        self.export_path = self.get_abs_path(export_path)
        if not os.path.exists(self.export_path):
            os.makedirs(self.export_path)
        self.export_path = os.path.join(self.export_path, self.atomic.attack_technique)
        if not os.path.exists(self.export_path):
            os.makedirs(self.export_path)

    def execute(self):
        # generate single markdown file for the atomic
        self.generate_atomic_markdown_documents()
        # add to different matricies files if applicable
       # print(Matrices().execute(self.atomic))
        # add to markdown indexes
        # add to csv indexes
        # create attack navigator layers
        
        pass
        
    def generate_atomic_markdown_documents(self):
        template = self.get_template(self.atomic_markdown_template)
        with open(os.path.join(self.export_path, f"{self.atomic.attack_technique}" + ".md"), 'w+') as file:
            file.write(template.render(attr.asdict(self.atomic)))
