#!/usr/bin/env python3

import os
import requests
import json

project = os.environ['project']
environment = os.environ['environment']
status = True
author = os.environ['author']
hookUrl = os.environ['webhook'] #'https://hooks.slack.com/services/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'
departure = os.environ['departure']

color = 'ffffff'
statusText = ''
destination = ''

if status == True:
    color = '34795D'
    statusText = '*Succeed*'
else:
    color = 'ff0000'
    statusText = '*Failed*'

if environment == 'staging':
    departure = 'feature/aaaa' # PR branch name
    destination = 'develop'
elif environment == 'production':
    departure = '1.0.0' # Tags
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

print(section)

# Attachments
attachments = {'attachments': [{'color': color, 'blocks': blocks}]}

requests.post(
    hookUrl, 
    data=json.dumps(attachments), 
    headers={'Content-Type': 'application/json'}
)