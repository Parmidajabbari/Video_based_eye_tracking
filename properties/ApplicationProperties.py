class PropertyManager:
    def __init__(self, file_path):
        self.properties = {}
        self.load_properties(file_path)

    def load_properties(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    self.properties[key.strip()] = value.strip()

    def get_value(self, key):
        return self.properties.get(key)


class ApplicationProperties:
    def __init__(self):
        self.property_manager = PropertyManager('../properties/EyeTracker.properties')

    @property
    def debug(self):
        return self.property_manager.get_value('App.DEBUG')

    @property
    def video_source(self):
        return self.property_manager.get_value('Video.VIDEO_SOURCE')

    @property
    def frame_save_path(self):
        return self.property_manager.get_value('Video.FRAME_SAVE_PATH')

    @property
    def log_file(self):
        return self.property_manager.get_value('Logging.LOG_FILE')

    @property
    def log_level(self):
        return self.property_manager.get_value('Logging.LOG_LEVEL')

    @property
    def log_format(self):
        return self.property_manager.get_value('Logging.LOG_FORMAT')

    @property
    def active_form_id(self):
        return self.property_manager.get_value('Form.ACTIVE_FORM_ID')