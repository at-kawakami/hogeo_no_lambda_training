import boto3
import json
import logging
import os

from base64 import b64decode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

SLACK_CHANNEL = os.environ['slackChannel']
HOOK_URL = os.environ['HookUrl']
print(HOOK_URL)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Event: " + str(event))
    message = json.loads(event['Records'][0]['Sns']['Message'])
    logger.info("Message: " + str(message))

    alarm_name = message['detail']['project-name']
    new_state = message['detail']['build-status']
    exception_name = message['detail']['error']
    cause = message['detail']['cause']
    
    if 'slack-channel' in message['detail']:
        SLACK_CHANNEL = message['detail']['slack-channel']    
    else:
        SLACK_CHANNEL = os.environ['slackChannel']

    slack_message = {
        'channel': SLACK_CHANNEL,
        "attachments": [
            {
                "color": "#ff3333",
                "title": alarm_name,
                "fields": [
                    {
                        "title": "Name",
                        "value": exception_name
                    },
                    {
                        "title": "Reason",
                        "value": cause
                    }
                ]
            }
        ]
    }

    req = Request(HOOK_URL, json.dumps(slack_message).encode('utf-8'))
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to %s", slack_message['channel'])
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)