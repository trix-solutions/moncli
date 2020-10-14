import json

class MondayClientCredentials():

    def __init__(self, api_key_v1: str, api_key_v2: str):
        self.api_key_v1 = api_key_v1
        self.api_key_v2 = api_key_v2


class Column():

    def __init__(self, **kwargs):
        self.id = kwargs['id']

        for key, value in kwargs.items():

            if key == 'archived':
                self.archived = value

            elif key == 'settings_str':
                self.settings_str = value

            elif key == 'title':
                self.title = value
            
            elif key == 'type':
                self.type = value

            elif key == 'width':
                self.width = value

            elif key == 'board_id':
                self.board_id = value

        # Load settings string
        try:
            settings_str = json.loads(self.settings_str)
            if self.type == 'color':
                self.settings = StatusSettings(**settings_str)
        except:
            pass


class Notification():

    def __init__(self, **kwargs):
        self.id = kwargs['id']

        for key, value in kwargs.items():

            if key == 'text':
                self.text = value


class Tag():

    def __init__(self, **kwargs):

        self.id = kwargs['id']

        for key, value in kwargs.items():

            if key == 'name':
                self.name = value

            elif key == 'color':
                self.color = value


class Plan():

    def __init__(self, **kwargs):

        for key, value in kwargs.items():

            if key == 'max_users':
                self.max_users = value

            elif key == 'period':
                self.period = value

            elif key == 'tier':
                self.tier = value

            elif key == 'version':
                self.version = value


class Asset():

    def __init__(self, **kwargs):

        for key, value in kwargs.items():

            if key == 'created_at':
                self.created_at = value

            elif key == 'file_extension':
                self.file_extension = value

            elif key == 'file_size':
                self.file_size = value

            elif key == 'id':
                self.id = value

            elif key == 'name':
                self.name = value

            elif key == 'public_url':
                self.public_url = value

            elif key == 'uploaded_by':
                self.uploaded_by = value

            elif key == 'url':
                self.url = value

            elif key == 'url_thumbnail':
                self.url_thumbnail = value


class StatusSettings():

    def __init__(self, **kwargs):
        self.labels = kwargs['labels']

        for key, value in kwargs.items():

            if key == 'done_colors':
                self.done_colors = value

            elif key == 'sumType':
                self.sum_type = value

            elif key == 'color_mapping':
                self.color_mapping = value

            elif key == 'labels_positions_v2':
                self.labels_positions_v2 = value


    def get_index(self, label: str):

        for key, value in self.labels.items():

            if value == label:
                return int(key)

        return None