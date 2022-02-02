import os
from os.path import isfile, join
import json
import glob

class StringUtils:
    def extract_text_from_html(self, source, strAfter='\'>', strUntil='</'):
        startIndex = source.find(strAfter) + len(strAfter)
        endIndex = source.find(strUntil)
        return source[startIndex:endIndex]

class FileLoader:
    def load_file(self, path):
        content = {}

        if (isfile(path)):
            with open(path,) as file:
                content = json.load(file)
        else:
            print(f'{path} not found.')

        return content

    def load_files(self, path, recursive=True):
        teams = []

        for f in glob.iglob(path, recursive=recursive):
            with open(f,) as file:
                teams.append(json.load(file))

        return teams

class ConfigurationLoader:
    def __init__(self, fileLoader, path):
        self.config = fileLoader.load_file(path)

    def get_config_value(self, key):
        # Try get config from environment variable
        try:
            return os.environ[key]
        except KeyError:
            print(f'{key} not found in env variable.')

        print(f'Attempting to load {key} from config..')

        return self.config[key]