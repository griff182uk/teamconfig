class Team:
    def __init__(self):
        self.name = ''
        self.channels = []

class Channel:
    def __init__(self):
        self.name = ""
        self.description = ""

    def __init__(self, name, description):
        self.name = name
        self.description = description

class Project:
    def __init__(self):
        self.name = ''
        self.description = ''