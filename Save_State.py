import json
import yaml
from App_Configs import App_Configs
from pathlib import Path
from Abstract_State import Abstract_State

class Save_State:

    CONFIG_DIRECTORY = "./configs"
    save_state_file = None

    init = Abstract_State.init.copy()
    create_state = Abstract_State.create_state.copy()
    liking_state = Abstract_State.liking_state.copy()
    rating_state = Abstract_State.rating_state.copy()

    @classmethod
    def init_state_file(cls, filename):
        print("#########################################################")
        print("#########      Save_State - init_state_file()  ##########")
        print("#########################################################")
        cls.save_state_file = filename # "zConfg_local.zstate.yaml"

        if cls._is_file_exists():
            print("Save_State - Checking previous file...")
            cls.file_into_this()
        else:
            print("Save_State - Creating new state!")
            App_Configs.create_new_file(cls.save_state_file)

    @classmethod
    def file_into_this(cls):
        # print("####################################################")
        # print("#####       Save_State - file_into_this()     ######")
        # print("#####################################################")
        # print("    Save_State - file_into_this(): ", cls.save_state_file)
        file_path = f"{cls.CONFIG_DIRECTORY}/{cls.save_state_file}"
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            datainit = data.get('init', {})

            cls.init['SELENIUM_IS_HEADLESS']    = data['init']['SELENIUM_IS_HEADLESS'] 
            cls.init['ENV']                     = data['init']['ENV'] 
            cls.init['EMAIL']                   = data['init']['EMAIL'] 
            cls.init['PWORD']                   = data['init']['PWORD'] 
            cls.init['CREATE_BOT_START']        = data['init']['CREATE_BOT_START'] 
            cls.init['CREATE_BOT_END_BEFORE']   = data['init']['CREATE_BOT_END_BEFORE'] 
            cls.init['LIKE_BOT_START']          = data['init']['LIKE_BOT_START'] 
            cls.init['LIKE_BOT_END_BEFORE']     = data['init']['LIKE_BOT_END_BEFORE'] 
            cls.init['LIKE_PAGES']              = data['init']['LIKE_PAGES']
            
            # anachronistic coding/im-lazy
            cls.init['RATE_BOT_START']          = datainit.get('RATE_BOT_START', None)
            cls.init['RATE_BOT_END_BEFORE']     = datainit.get('RATE_BOT_END_BEFORE', None)
            cls.init['RATE_PAGE']               = datainit.get('RATE_PAGE', None)

            cls.create_state['email_index_finished'] = data['create_state']['email_index_finished']
            cls.liking_state['email_index_finished'] = data['liking_state']['email_index_finished']
            cls.rating_state['email_index_finished'] = data['rating_state']['email_index_finished'] if data.get('rating_state', None) else None

            # cls.rating_state['email_index_finished'] = data['rating_state']['email_index_finished']

        return data        

    @classmethod
    def update_state_file(cls):
        # print("############################################################")
        # print("#########      Save_State - update_state_file()     ########")
        # print("############################################################")
        yaml_data = {}
        yaml_data['init'] = App_Configs.init
        yaml_data['create_state'] = App_Configs.create_state
        yaml_data['liking_state'] = App_Configs.liking_state
        yaml_data['rating_state'] = App_Configs.rating_state

        yaml_content = yaml.dump(yaml_data, default_flow_style=False)
        file_path = f"{cls.CONFIG_DIRECTORY}/{cls.save_state_file}"
        with open(file_path, 'w') as file:
            file.write(yaml_content)

    @classmethod
    def state_into_app_configs(cls):
        print("###############################################################")
        print("#########      Save_State - state_into_app_configs()     #########")
        print("###############################################################")
        App_Configs.init['SELENIUM_IS_HEADLESS']    = cls.init['SELENIUM_IS_HEADLESS']
        App_Configs.init['ENV']                     = cls.init['ENV']
        App_Configs.init['EMAIL']                   = cls.init['EMAIL']
        App_Configs.init['PWORD']                   = cls.init['PWORD']
        App_Configs.init['CREATE_BOT_START']        = cls.init['CREATE_BOT_START']
        App_Configs.init['CREATE_BOT_END_BEFORE']   = cls.init['CREATE_BOT_END_BEFORE']
        App_Configs.init['LIKE_BOT_START']          = cls.init['LIKE_BOT_START']
        App_Configs.init['LIKE_BOT_END_BEFORE']     = cls.init['LIKE_BOT_END_BEFORE']
        App_Configs.init['LIKE_PAGES']              = cls.init['LIKE_PAGES']
        App_Configs.init['RATE_BOT_START']          = cls.init['RATE_BOT_START']
        App_Configs.init['RATE_BOT_END_BEFORE']     = cls.init['RATE_BOT_END_BEFORE']
        App_Configs.init['RATE_PAGE']               = cls.init['RATE_PAGE']

        App_Configs.create_state['email_index_finished'] = cls.create_state['email_index_finished']
        App_Configs.liking_state['email_index_finished'] = cls.liking_state['email_index_finished']
        App_Configs.rating_state['email_index_finished'] = cls.rating_state['email_index_finished']

    @classmethod
    def _is_file_exists(cls):
        file_path = Path(f"{cls.CONFIG_DIRECTORY}/{cls.save_state_file}")
        if file_path.exists():
            return True
        else:
            return False
    