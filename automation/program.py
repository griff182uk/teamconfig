import os
from mappers import mappers
from modules import slack, azdevops
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
    stringUtils = utils.StringUtils()
    fileLoader = utils.FileLoader()
    teamConfigDataMapper = mappers.TeamConfigCommunicationDataMapper(fileLoader, stringUtils)

    appSettings = fileLoader.load_file(os.path.join('automation', 'automation.config.json'))
    modulesSettings = appSettings['modules']
    
    slackManagerApp = slack.SlackManagerApp(modulesSettings['slack'], teamConfigDataMapper)
    azDevopsManagerApp = azdevops.AzureDevOpsManager(modulesSettings['azdevops'], teamConfigDataMapper)
    
    return {
        "stringUtils": stringUtils,
        "fileLoader": fileLoader,
        "teamConfigDataMapper": teamConfigDataMapper,
        "modules": [
            slackManagerApp, 
            azDevopsManagerApp
        ]
    }

def run():
    set_context()
    services = start_up()
    modules = services["modules"]
    for module in modules:
        module.run()

run()