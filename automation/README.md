# Automation
This folder will contain scripts that can be used to automate much of the setup of an organisation based on the configuration generated by the `teamconfig` project.

## Slack Channel Generator
### Disclaimer
This script is just a prof of concept right now. Apologies in advanced - my python skills are a little rusty.

### Introduction
This is just a simple script to generate Slack channels based on the teams configuration generated in the main `teamconfig` application.

### Using the script
This script makes use of the [Slack API](https://api.slack.com/methods/conversations.create). In order to integrate with Slack, we are required to create an app to act as an identity which will make changes to your workspace on your behalf via the API.

### Installing the Team Configurator
Slack App in review process. 

TODO: This section needs work.

Browse slack apps and install an app called 'Team Configurator'. This acts an identity for the API calls. You will need this apps bot token from the settings, if available. This is potentially accessible in the app settings, but I need to verify this.

### Creating a slack bot app
Alternatively, you can create a slack app / bot for free that is private to your organisation using [this guide](https://api.slack.com/authentication/basics). If you do this, under the 'Features > OAuth & Permissions > Scopes' section, add the following:

```text
channels:manage
channels:read
groups:read
im:read
mpim:read
```

If you'd like this application to be defined in code and live in source control, you can also create an app [here](https://api.slack.com/apps?new_app=1) using an app manifest (hit 'Create New App' and hit 'From an app manifest'). An example app manifest would be:

```yml
display_information:
  name: workspace-admin
features:
  bot_user:
    display_name: workspace-admin
    always_online: false
oauth_config:
  scopes:
    bot:
      - channels:manage
      - channels:read
      - groups:read
      - im:read
      - mpim:read
settings:
  org_deploy_enabled: false
  socket_mode_enabled: false
  token_rotation_enabled: false
```

Once the app is created and installed onto your workspace, take the bot token from the 'Oauth & Permissions' screen and place in the `slack.config.json` file for this app (see next section).

### Script Configuration
In order to use this script, you will need to add a `slack.config.json` file in the `/automation/integrations/` directory. This should contain some JSON that will store your bot token locally. It has been excluded in the `.gitignore` file. This is temporary, until such time OAuth can be implemented. You can make a copy of the `slack.config.json.example` file to get a template and remove the `.example` extension.

```json
{
    "API_TOKEN": "xoxb-XXX..."
}
```

### Possible uses

We could plumb this script into a CI/CD pipeline that will run everytime the 'teams' folder inthe project is updated.

### Notes

At this time, this script doesn't treat this project as declarative. Therefore changes to channel names will result in new channels. How this will work is yet to be decided.