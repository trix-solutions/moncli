from moncli.routes import constants
from moncli.routes.requests import execute_get

def get_tag_by_id(api_key, tag_id):

    resource_url = constants.TAGS_BY_ID.format(tag_id)

    return execute_get(api_key, resource_url)