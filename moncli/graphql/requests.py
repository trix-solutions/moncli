import requests, json
from moncli.graphql import GraphQLOperation, OperationType

def execute_query(api_key: str, **kwargs):

    query = None
    variables = None
    for key, value in kwargs.items():
        if query == None and key == 'operation':
            query = value.format_body()
        elif query == None and key == 'query':
            query = value
        elif variables == None and key == 'variables':
            variables = value

    headers = { 'Authorization': api_key }
    data = { 'query': query, 'variables': variables }

    resp = requests.post(
        'https://api.monday.com/v2',
        headers=headers,
        data=data)

    if resp.status_code == 200:
        text = resp.json()
        return text['data']

    