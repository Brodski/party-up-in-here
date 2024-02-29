import json
import yaml
from App_Configs import App_Configs
from pathlib import Path

class Save_State:

    save_state_file = None
    initialization = {}
    create_state = {}
    liking_state = {}

    initialization['SELENIUM_IS_HEADLESS'] = None
    initialization['ENV'] = None
    initialization['EMAIL'] = None
    initialization['PWORD'] = None
    initialization['CREATE_BOT_START'] = None
    initialization['CREATE_BOT_END_BEFORE'] = None
    initialization['LIKE_BOT_START'] = None
    initialization['LIKE_BOT_END_BEFORE'] = None
    initialization['LIKE_PAGES'] = None

    create_state['at_email_index'] = None

    liking_state['at_email_index'] = None
    liking_state['at_page'] = None

    # def __init__(self, filename=".env_config_local", **kwargs):
    def __new__(cls, filename):
        print("SAVE STATE __new__")
        cls.save_state_file = filename + ".save_state.yaml"
        
        if cls._is_file_exists():
            # cls._init_save_state()
            cls._load_save_state()
            print("LAOD COMPELTED!")
            print(json.dumps(cls.initialization, indent=4, sort_keys=False))
        else:
            cls._init_save_state()

        data = cls._load_save_state()
        print(json.dumps(data, indent=4, sort_keys=False))

    @classmethod
    def _is_file_exists(cls):
        file_path = Path(cls.save_state_file)
        if file_path.exists():
            return True
        else:
            return False
    

    @classmethod
    def _init_save_state(cls):
        data = {}
        data['initialization'] = {}
        for attr in dir(App_Configs):
            if not attr.startswith("__") and not callable(getattr(App_Configs, attr)): # Check if the attribute is not a built-in attribute and is not callable (to filter out methods)
                value = getattr(App_Configs, attr)
                data['initialization'][attr] = value
        # for attribute, value in self.config_varz.__dict__.items():
        #     data['initialization'][attribute] = value
        print("CREATED SAVE STATE")

        data['create_state'] = {}
        data['create_state']['at_email_index'] = None

        data['liking_state'] = {}
        data['liking_state']['at_email_index'] = None
        data['liking_state']['at_page'] = None

        with open(cls.save_state_file, 'w') as file:
            yaml.dump(data, file, sort_keys=False, default_flow_style=False, indent=2)

    @classmethod
    def _load_save_state(cls):
        print("reading save_state file: ", cls.save_state_file)
        with open(cls.save_state_file, 'r') as file:
            data = yaml.safe_load(file)
            cls.initialization['SELENIUM_IS_HEADLESS']    = data['initialization']['SELENIUM_IS_HEADLESS'] 
            cls.initialization['ENV']                     = data['initialization']['ENV'] 
            cls.initialization['EMAIL']                   = data['initialization']['EMAIL'] 
            cls.initialization['PWORD']                   = data['initialization']['PWORD'] 
            cls.initialization['CREATE_BOT_START']        = data['initialization']['CREATE_BOT_START'] 
            cls.initialization['CREATE_BOT_END_BEFORE']   = data['initialization']['CREATE_BOT_END_BEFORE'] 
            cls.initialization['LIKE_BOT_START']          = data['initialization']['LIKE_BOT_START'] 
            cls.initialization['LIKE_BOT_END_BEFORE']     = data['initialization']['LIKE_BOT_END_BEFORE'] 
            cls.initialization['LIKE_PAGES']              = data['initialization']['LIKE_PAGES']
        return data        

    def update_liking(self):
        pass

    def update_creating(self):
        pass

    def save_single(self):

        filename = 'app_config.yaml'
        with open(filename, 'r') as file:
            data = yaml.safe_load(file)

        if 'application' in data:
            data['application']['description'] = 'This is an updated description.'

        # Write the updated data back to the YAML file
        with open(filename, 'w') as file:
            yaml.dump(data, file, sort_keys=False, default_flow_style=False, indent=2)