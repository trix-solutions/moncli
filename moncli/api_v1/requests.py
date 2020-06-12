from moncli.routes import MondayQueryParameters, format_url, raise_mondayapi_error
from .. import constants
import requests, json


def execute_get(api_key, resource_url, params = None):

    monday_params = MondayQueryParameters(api_key)

    if params != None:
        monday_params.add_params(params)

    resp = requests.get(
        format_url(resource_url), 
        params=monday_params.to_dict(),
        timeout=constants.TIMEOUT)

    if resp.status_code == 200:
        return resp.json()

    raise_mondayapi_error('GET', resource_url, resp)


def execute_post(api_key, resource_url, body):

    monday_params = MondayQueryParameters(api_key)

    resp = requests.post(
        format_url(resource_url),
        body,
        params=monday_params.to_dict(),
        timeout=constants.TIMEOUT)

    if resp.status_code == 200 or resp.status_code == 201:
        return resp.json()

    raise_mondayapi_error('POST', resource_url, resp)


def execute_put(api_key, resource_url, body):

    monday_params = MondayQueryParameters(api_key)

    data = json.dumps(body)

    resp = requests.post(
        format_url(resource_url),
        data,
        params=monday_params.to_dict(),
        timeout=constants.TIMEOUT)

    if resp.status_code == 200:
        return resp.json()

    raise_mondayapi_error('PUT', resource_url, resp)


def execute_delete(api_key, resource_url, params = None):

    monday_params = MondayQueryParameters(api_key)

    if params != None:
        monday_params.add_params(params)

    resp = requests.delete(
        format_url(resource_url), 
        params=monday_params.to_dict(),
        timeout=constants.TIMEOUT)

    if resp.status_code == 200:
        return resp.json()

    raise_mondayapi_error('GET', resource_url, resp)