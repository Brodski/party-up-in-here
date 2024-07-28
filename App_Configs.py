import re
from dotenv import dotenv_values
import yaml
from Abstract_State import Abstract_State

class App_Configs:
    init = Abstract_State.init.copy()
    create_state = Abstract_State.create_state.copy()
    liking_state = Abstract_State.liking_state.copy()
    rating_state = Abstract_State.rating_state.copy()

    CONFIG_DIRECTORY = "./configs"

    @classmethod
    def prep_state_filename(cls, filename):
        return f"{filename}.zstate.yaml"
         
    def __new__(cls, file=None):
            instance = super(App_Configs, cls).__new__(cls)
            if (file != None):
                env_vars = dotenv_values(f"{cls.CONFIG_DIRECTORY}/{file}")  
                cls.create_state['email_index_finished'] = None
                cls.liking_state['email_index_finished'] = None
                cls.rating_state['email_index_finished'] = None
                
                cls.init['SELENIUM_IS_HEADLESS']   = env_vars['SELENIUM_IS_HEADLESS']
                cls.init['ENV']                    = env_vars['ENV']
                cls.init['EMAIL']                  = env_vars['EMAIL']
                cls.init['PWORD']                  = env_vars['PWORD']
                cls.init['CREATE_BOT_START']       = int(env_vars['CREATE_BOT_START'])
                cls.init['CREATE_BOT_END_BEFORE']  = int(env_vars['CREATE_BOT_END_BEFORE'])
                cls.init['LIKE_BOT_START']         = int(env_vars['LIKE_BOT_START'])
                cls.init['LIKE_BOT_END_BEFORE']    = int(env_vars['LIKE_BOT_END_BEFORE'])

                # anachronistic coding/im-lazy
                cls.init['RATE_BOT_START']          = int(env_vars.get('RATE_BOT_START')) if env_vars.get('RATE_BOT_START', None) else None
                cls.init['RATE_BOT_END_BEFORE']     = int(env_vars.get('RATE_BOT_END_BEFORE')) if env_vars.get('RATE_BOT_END_BEFORE', None) else None
                cls.init['RATE_PAGE']               = env_vars.get('RATE_PAGE', None)

                LIKE_PAGES_aux = re.sub(r'\s+', "", env_vars['LIKE_PAGES']).split(',')
                LIKE_PAGES_aux = LIKE_PAGES_aux if LIKE_PAGES_aux[-1] != "" else LIKE_PAGES_aux[:-1] # incase last ele ends with ,
                cls.init['LIKE_PAGES'] = [page for page in LIKE_PAGES_aux if (page[0] != "#" and page[:2] != "//")] # filter out "comments" eg # and //

            return instance

    
    @classmethod
    def create_new_file(cls, file_name):
        # print("####################################################")
        # print("#####      App_Configs - create_new_file()     #####")
        # print("####################################################")
        data = {}
        for attr in dir(App_Configs):
            if not attr.startswith("__") and not callable(getattr(App_Configs, attr)): # Check if the attribute is not a built-in attribute and is not callable (to filter out methods)
                value = getattr(App_Configs, attr)
                data[attr] = value
                # print("create_new_file - attr,value:", attr, value)


        file_path = f"{cls.CONFIG_DIRECTORY}/{file_name}"
        with open(file_path, 'w') as file:
            yaml.dump(data, file, sort_keys=False, default_flow_style=False, indent=2)
