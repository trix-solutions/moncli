import requests, json, time

from .. import constants
from . import MondayApiError


def execute_query(api_key: str, timeout=constants.TIMEOUT, **kwargs):

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

    return _process_repsonse(api_key, timeout, resp, data, **kwargs)


def upload_file(api_key: str, file_path: str, timeout = constants.TIMEOUT, **kwargs):

    query = None
    for key, value in kwargs.items():
        if query == None and key == 'operation':
            query = value.format_body()

    headers = { 'Authorization': api_key }
    data = { 'query': query }
    files = { 'variables[file]': open(file_path, 'rb') }

    resp = requests.post(
        constants.API_V2_FILE_ENDPOINT,
        headers=headers,
        data=data,
        files=files,
        timeout=timeout)

    return _process_repsonse(api_key, timeout, resp, data, **kwargs)
    

def _process_repsonse(api_key: str, timeout: int, resp, data, **kwargs):
    
    text: dict = resp.json()

    if resp.status_code == 403 or resp.status_code == 500:
        raise MondayApiError(json.dumps(data), resp.status_code, '', [text['error_message']])
    if text.__contains__('errors'):
        if not 'Query has complexity of' in errors[0]['message']: # May my sins be forgiven someday...
            error_query = json.dumps(data)
            status_code = resp.status_code
            errors = text['errors']
            raise MondayApiError(error_query, status_code, '', errors)
        # Wait for 5 seconds and try again in case of rate limiting... ^
        time.sleep(5)
        return execute_query(api_key, timeout, **kwargs)
    # Raise exception for parse errors.
    if text.__contains__('error_code'):
        error_query = json.dumps(data)
        raise MondayApiError(error_query, 400, text['error_code'], text['error_message'])

    return text['data']