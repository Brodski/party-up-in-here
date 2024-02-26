import re
from dotenv import dotenv_values

class AppConfigSingleton:
    _instance = None
    _is_initialized = False  # Add an initialization flag
    
    # env_vars = dotenv_values(file)  
    # SELENIUM_IS_HEADLESS = env_vars['SELENIUM_IS_HEADLESS']
    # ENV = env_vars['ENV']
    # EMAIL = env_vars['EMAIL']
    # PWORD = env_vars['PWORD']
    # CREATE_BOT_START = env_vars['CREATE_BOT_START']
    # CREATE_BOT_END = env_vars['CREATE_BOT_END']
    # LIKE_BOT_START = env_vars['LIKE_BOT_START']
    # LIKE_BOT_END_BEFORE = env_vars['LIKE_BOT_END_BEFORE']

    # _like_pages_aux = re.sub(r'\s+', "", env_vars['LIKE_PAGES']).split(',')
    # LIKE_PAGES = _like_pages_aux if _like_pages_aux[-1] != "" else _like_pages_aux[:-1]


    
    def __new__(cls, file=None): # file is requried
        if cls._instance is None:
            cls._instance = super(AppConfigSingleton, cls).__new__(cls)
        return cls._instance

    def __init__(self, file=None): #optional
        if not self._is_initialized:
            env_vars = dotenv_values(file)  
            self.SELENIUM_IS_HEADLESS   = env_vars['SELENIUM_IS_HEADLESS']
            self.ENV                    = env_vars['ENV']
            self.EMAIL                  = env_vars['EMAIL']
            self.PWORD                  = env_vars['PWORD']
            self.CREATE_BOT_START       = int(env_vars['CREATE_BOT_START'])
            self.CREATE_BOT_END_BEFORE  = int(env_vars['CREATE_BOT_END_BEFORE'])
            self.LIKE_BOT_START         = int(env_vars['LIKE_BOT_START'])
            self.LIKE_BOT_END_BEFORE    = int(env_vars['LIKE_BOT_END_BEFORE'])

            LIKE_PAGES_aux = re.sub(r'\s+', "", env_vars['LIKE_PAGES']).split(',')
            LIKE_PAGES_aux = LIKE_PAGES_aux if LIKE_PAGES_aux[-1] != "" else LIKE_PAGES_aux[:-1] # incase last ele ends with ,
            self.LIKE_PAGES = [page for page in LIKE_PAGES_aux if (page[0] != "#" and page[:2] != "//")] # filter out "comments" eg # and //

            self._is_initialized = True  # Set the flag to True after initialization
