from enum import Enum
from typing import List, Dict


class CommandType(Enum):
    ADD = 1
    SET = 2



class Statement:

    def __init__(self, command: CommandType, path: str, properties: List = [], condition: str = None):
        self.properties = properties
        self.command = command
        self.path = path
        self.condition = condition

    def export(self):
        buffer = f"/{self.path} {self.command.name.lower()}"
        if self.condition is not None and self.condition != '':
            buffer += f" [ {self.condition} ]"
        for prop in self.properties:
            key = list(prop.keys())[0]
            if prop[key] is None:
                buffer += f" {key}"
            elif ' ' in str(prop[key]) or '=' in str(prop[key]):
                buffer += f' {key}="{prop[key]}"'
            else:
                buffer += f" {key}={prop[key]}"
        return buffer

    def __str__(self):
        return self.export()

    def __repr__(self):
        return self.export()

