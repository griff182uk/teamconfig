import os
from os.path import isfile, join
import json
import glob
import requests

def set_context():
    scriptLocation = os.path.dirname(os.path.abspath(__file__))
    print(f'Script location: {scriptLocation}')

    referenceFolder = f'{os.path.sep}app'
    print(f'Attempting to find specific folder in script path for reference: {referenceFolder}')
    endIndex = scriptLocation.find(f'{referenceFolder}')

    if (endIndex > -1):
        print('Reference folder found in script path.')
        basePath = scriptLocation[0:endIndex]

        print(f'Changing directory to desired root folder.')
        os.chdir(basePath)
        print(f'Context changed to: {basePath}')
    else:
        print('Reference folder not found in script path. Exiting script.')
        exit()

def get_api_token(medium):
    # Try get config from environment variable
    try:
        return os.environ['API_TOKEN']
    except KeyError:
        print('API_TOKEN not found in env variable.')

    print(f'Attempting to load API_TOKEN from {medium}.config.json..')
    config = load_config_file(medium)

    return config['API_TOKEN']

def load_config_file(medium):
    configFile = os.path.join(f'.{os.path.sep}', 'app', 'comms-gen', medium, 'config.json')
    config = {}

    if (isfile(configFile)):
        with open(configFile,) as file:
            config = json.load(file)
    else:
        print('config.json not found.')

    return config

def load_teams_configuration():
    print('Loading teams config..')

    teams = []
    teamsDir = os.path.join(f'.{os.path.sep}', 'teams', '*.json')

    for f in glob.iglob(teamsDir, recursive=True):
        with open(f,) as file:
            teams.append(json.load(file))

    print('Teams config loaded.')

    return teams

def extract_text_from_html(source, strAfter='\'>', strUntil='</'):
    startIndex = source.find(strAfter) + len(strAfter)
    endIndex = source.find(strUntil)

    return source[startIndex:endIndex]

def extract_comms_data(rawTeamsData, medium):
    print('Extracting teams comms data..')

    teams = []

    for t in rawTeamsData:
        team = {}
        team['name'] = t['overview']['name']
        for comm in t['communications']:
            if (comm['medium'].lower() == medium.lower()):
                team['channels'] = []
                for channel in comm['channels']:
                    name = ''

                    # TODO: Remove temp code when schema changes the name field from a html anchor tag to a true name
                    if (str(channel['name']).lower().__contains__('<a href')):
                        name = extract_text_from_html(channel['name'])
                    else:
                        name = channel['name']

                    myChannel = {
                        'name': name,
                        'description': channel['description']
                    }
                    team['channels'].append(myChannel)

        teams.append(team)

    print('Teams comms data extracted.')

    return teams

def generate_slack_channels(apiToken, teamsData):
    print('Generating slack channels..')

    baseUrl = 'https://slack.com/api/conversations.create?name={}'
    headers = {'Authorization': f'Bearer {apiToken}'}

    for team in teamsData:
        print(f'Generating slack channels for {team["name"]}..')

        for channel in team['channels']:
            channelName = channel['name']
            url = baseUrl.format(channelName)
            response = requests.post(url, headers=headers)
            # response = requests.post('https://slack.com/api/conversations.create?name=python-test', headers=headers)
            if (not response.ok):
                print(f'Something went wrong creating {channelName}. Reason: {response.reason}. Exiting script.')
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

        print(f"Done generating slack channels for {team['name']}.")

    print('Slack channels generated.')

def main():
    set_context()
    medium = 'slack'
    apiToken = get_api_token(medium)
    # print(apiToken)
    rawTeamsData = load_teams_configuration()
    # print(rawTeamsData)
    transformedTeamsData = extract_comms_data(rawTeamsData, medium)
    # print(transformedTeamsData)
    generate_slack_channels(apiToken, transformedTeamsData)

main()