import os
from mappers import mappers
from integrations import slack
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from lib import utils

def set_context():
    scriptDirectory = os.path.dirname(os.path.abspath(__file__))
    repoRootDirectory = os.path.dirname(scriptDirectory)

    print(f'Changing directory to desired root folder.')
    os.chdir(repoRootDirectory)
    print(f'Context changed to: {repoRootDirectory}')

def start_up():
    configFile = os.path.join('automation', 'integrations', 'slack.config.json')
    stringUtils = utils.StringUtils()
    fileLoader = utils.FileLoader()
    config = utils.ConfigurationLoader(fileLoader, configFile)
    teamConfigDataMapper = mappers.TeamConfigCommunicationDataMapper(fileLoader, stringUtils)
    slackManagerApp = slack.SlackManagerApp(config, teamConfigDataMapper)

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
    app.run()

run()