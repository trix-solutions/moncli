import requests, json

from .. import constants
from . import MondayApiError

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
        constants.API_V2_ENDPOINT,
        headers=headers,
        data=data)

    text: dict = resp.json()

    if resp.status_code == 403 or resp.status_code == 500:
        raise MondayApiError(json.dumps(data), resp.status_code, [text['error_message']])

    if text.__contains__('errors'):
        error_query = json.dumps(data)
        status_code = resp.status_code
        errors = text['errors']
        raise MondayApiError(error_query, status_code, errors)

    return text['data']
