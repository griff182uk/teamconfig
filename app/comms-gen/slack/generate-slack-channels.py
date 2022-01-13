import os
from os.path import isfile, join
import json
import glob
import requests

def set_context():
    currentPath = os.path.dirname(os.path.abspath(__file__))
    endIndex = currentPath.find('/app')
    basePath = currentPath[0:endIndex]
    os.chdir(basePath)
    # print(os.getcwd())

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
    configFile = f'./app/comms-gen/{medium}/config.json'
    config = {}

    if (isfile(configFile)):
        with open(configFile,) as file:
            config = json.load(file)
    else:
        print('slack.config.json not found.')

    return config

def load_teams_configuration():
    print('Loading teams config..')

    teams = []
    teamsDir = './teams/*.json'

    for f in glob.iglob(teamsDir, recursive=True):
        with open(f,) as file:
            teams.append(json.load(file))

    print('Done.')

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

    print('Done.')

    return teams

def generate_slack_channels(apiToken, teamsData):
    print('Generating slack channels..')

    baseUrl = 'https://slack.com/api/conversations.create?name={}'
    headers = {'Authorization': f'Bearer {apiToken}'}

    for team in teamsData:
        print(f'Generating slack channels for {team["name"]}..')
        for channel in team['channels']:
            url = baseUrl.format(channel['name'])
            response = requests.post(url, headers=headers)
            # response = requests.post('https://slack.com/api/conversations.create?name=python-test', headers=headers)
            if (not response.ok):
                print(f'Something went wrong creating {channel["name"]}. Reason: {response.reason}')

            responseBody = response.json()
            if (not responseBody['ok'] and responseBody['error'].lower() == 'name_taken'):
                print(f'{channel["name"]} already exists')

        print(f"Done generating slack channels for {team['name']}.")

    print('Done.')

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