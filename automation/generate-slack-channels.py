import os
import requests
from mappers import mappers
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from lib import utils

class SlackManagerApp:
    def __init__(self, config, dataMapper):
        self.config = config
        self.dataMapper = dataMapper

    def generate_slack_channels(self):
        print('Generating slack channels..')

        baseUrl = 'https://slack.com/api/conversations.create?name={}'
        apiToken = self.config.get_config_value('API_TOKEN')
        headers = {'Authorization': f'Bearer {apiToken}'}
        teamsDataPath = os.path.join('teams', '*.json')
        teamsData = self.dataMapper.extract_comms_data_for_medium(teamsDataPath, 'slack')

        for team in teamsData:
            print(f'Generating slack channels for {team.name}..')

            for channel in team.channels:
                channelName = channel.name
                url = baseUrl.format(channelName)
                response = requests.post(url, headers=headers)
                # response = requests.post('https://slack.com/api/conversations.create?name=python-test', headers=headers)
                if (not response.ok):
                    print(f'Something went wrongstringUtils creating {channelName}. Reason: {response.reason}. Exiting script.')
                    exit()

                responseBody = response.json()

                if (not responseBody['ok'] and responseBody['error'].lower() == 'name_taken'):
                    print(f'{channelName} already exists')
                elif (not responseBody['ok'] and responseBody['error'].lower() == 'missing_scope'):
                    print(f'Token used does not have the following scopes configured: channels:manage, groups:write, im:write, mpim:write')
                    print('See docs here for further details: https://api.slack.com/methods/conversations.create')
                elif (not responseBody['ok']):
                    print(f'Error creating channel "{channelName}" Reason: {responseBody["error"].lower()}')
                else:
                    print(f'{channelName} created.')

            print(f"Done generating slack channels for {team.name}.")

        print('Slack channels generated.')

def set_context():
    scriptDirectory = os.path.dirname(os.path.abspath(__file__))
    repoRootDirectory = os.path.dirname(scriptDirectory)

    print(f'Changing directory to desired root folder.')
    os.chdir(repoRootDirectory)
    print(f'Context changed to: {repoRootDirectory}')

def start_up():
    configFile = os.path.join('automation', 'slack.config.json')
    stringUtils = utils.StringUtils()
    fileLoader = utils.FileLoader()
    config = utils.ConfigurationLoader(fileLoader, configFile)
    teamConfigDataMapper = mappers.TeamConfigCommunicationDataMapper(fileLoader, stringUtils)
    slackManagerApp = SlackManagerApp(config, teamConfigDataMapper)

    return {
        "stringUtils": stringUtils,
        "fileLoader": fileLoader,
        "teamConfigDataMapper": teamConfigDataMapper,
        "config": config,
        "app": slackManagerApp
    }

def run():
    set_context()
    services = start_up()
    app = services["app"]
    app.generate_slack_channels()

run()