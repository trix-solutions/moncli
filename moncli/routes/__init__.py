from .constants import BASE_URL, PORT, API_VERSION

def format_url(resource_url):

    return "{}:{}/{}/{}".format(
        BASE_URL, 
        PORT, 
        API_VERSION,
        resource_url)


def raise_mondayapi_error(method, resource_url, resp):
    
    raise MondayApiError(
        method, 
        format_url(resource_url), 
        resp.status_code,
         resp.text)


class MondayApiError(Exception):

    def __init__(self, method, error_url, error_code, message):

        self.method = method
        self.error_url = error_url
        self.error_code = error_code
        self.message = message


class MondayQueryParameters():

    def __init__(self, api_key):

        self.__dict = { 'api_key': api_key}


    def add_param(self, name, value):

        self.__dict[name] = value

    
    def add_params(self, params_dict):

        for key in params_dict:
            self.add_param(key, params_dict[key])

    
    def to_dict(self):

        return self.__dict