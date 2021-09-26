import os

import yaml


class YamlConfig:
    cur_path: str = os.path.dirname(os.path.abspath(__file__))
    
    def __init__(self, file_path: str = f"{cur_path}/config.yml") -> None:
        self.file_path = file_path
    
    def exists(self) -> bool:
        return os.path.exists(self.file_path)
    
    def load(self) -> dict:
        """
        :return: Return yaml data as dictionary format
        """
        with open(self.file_path, "r", encoding="utf-8") as yf:
            return yaml.load(yf, Loader=yaml.FullLoader)
    
    def write(self, data: dict) -> None:
        """
        Export yaml
        :param data: A dictionary of data that will be output in Yaml format
        """
        with open(self.file_path, "w", encoding="utf-8") as yf:
            yaml.dump(data, yf, default_flow_style=False)
