import requests, json

from moncli.constants import API_V2_ENDPOINT
from moncli.graphql.entities import MondayApiError

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
        API_V2_ENDPOINT,
        headers=headers,
        data=data)

    if resp.status_code != 200:
        pass

    text: dict = resp.json()

    if text.__contains__('errors'):
        error_query = json.dumps(data)
        status_code = resp.status_code
        errors = text['errors']
        raise MondayApiError(error_query, status_code, errors)

    return text['data']
