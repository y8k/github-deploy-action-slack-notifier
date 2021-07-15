#!/usr/bin/env python3

import os
import requests
import json

project = os.environ['INPUT_PROJECT']
environment = os.environ['INPUT_ENVIRONMENT']
status = os.environ['INPUT_STATUS']
author = os.environ['INPUT_AUTHOR']
hookUrl = os.environ['INPUT_WEBHOOK']
departure = os.environ['INPUT_DEPARTURE']

color = 'ffffff'
statusText = ''
destination = ''

if status == True:
    color = '34795D'
    statusText = '*Succeed*'
elif status == False:
    color = 'ff0000'
    statusText = '*Failed*'
else:
    color = 'ffffff'
    statusText = '*Undetermined*'

if environment == 'staging':
    destination = 'develop'
elif environment == 'production':
    destination = 'main'
else:
    departure = ''
    destination = 'unknown'


# Generate Header
message = f'*{project}* - Deploying is {statusText}'

headerText = {'type': 'mrkdwn', 'text': f'{message}'}
header = {'type': 'section', 'text': headerText}
fields = []

# Environment
if environment:
    environmentRow = {'type': 'mrkdwn', 'text': f'*Server Environment*:\n{environment}'}
    fields.append(environmentRow)

# Branch (PR)
if departure and destination:
    branchRow = {'type': 'mrkdwn', 'text': f'*Distribution*:\n{departure} -> {destination}'} 
    fields.append(branchRow)

# Author
if author:
    authorRow = {'type': 'mrkdwn', 'text': f'*Author*:\n{author}'}
    fields.append(authorRow)

# Section
section = {}
if len(fields) > 0:
    section = {'type': 'section', 'fields': fields}

# Context
context = {'type': 'context', 'elements': [{'type': 'mrkdwn', 'text': 'Check this result @on.sqd'}]}

# Blocks
blocks = [header, section, context]

# Attachments
attachments = {'attachments': [{'color': color, 'blocks': blocks}]}

requests.post(
    hookUrl, 
    data=json.dumps(attachments), 
    headers={'Content-Type': 'application/json'}
)