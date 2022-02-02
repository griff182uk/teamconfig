import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from models import models

class TeamConfigCommunicationDataMapper:
    def __init__(self, fileLoader, stringUtils):
        self.fileLoader = fileLoader
        self.stringUtils = stringUtils

    def extract_comms_data_for_medium(self, rawTeamsDataPath, medium):
        print('Extracting teams comms data..')

        rawTeamsData = self.fileLoader.load_files(rawTeamsDataPath)

        teams = []

        for t in rawTeamsData:
            team = models.Team()
            team.name = t['overview']['name']
            for comm in t['communications']:
                if (comm['medium'].lower() == medium.lower()):
                    for channel in comm['channels']:
                        name = ''

                        # TODO: Remove temp code when schema changes the name field from a html anchor tag to a true name
                        if (str(channel['name']).lower().__contains__('<a href')):
                            name = self.stringUtils.extract_text_from_html(channel['name'])
                        else:
                            name = channel['name']

                        myChannel = models.Channel(name, channel['description'])
                        
                        team.channels.append(myChannel)

            teams.append(team)

        print('Teams comms data extracted.')

        return teams