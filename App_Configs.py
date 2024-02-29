import re
from dotenv import dotenv_values

class App_Configs:
    # _instance = None
    # _is_initialized = False
    SELENIUM_IS_HEADLESS = None
    ENV = None
    EMAIL = None
    PWORD = None
    CREATE_BOT_START = None
    CREATE_BOT_END_BEFORE = None
    LIKE_BOT_START = None
    LIKE_BOT_END_BEFORE = None
    LIKE_PAGES = None

    # def __new__(cls, file=None): # file is requried
    #     if cls._instance is None:
    #         cls._instance = super(AppConfigSingleton, cls).__new__(cls)
    #     return cls._instance
    def __new__(cls, file=None):
            instance = super(App_Configs, cls).__new__(cls)
            if (file != None):
                env_vars = dotenv_values(file)  
                cls.SELENIUM_IS_HEADLESS   = env_vars['SELENIUM_IS_HEADLESS']
                cls.ENV                    = env_vars['ENV']
                cls.EMAIL                  = env_vars['EMAIL']
                cls.PWORD                  = env_vars['PWORD']
                cls.CREATE_BOT_START       = int(env_vars['CREATE_BOT_START'])
                cls.CREATE_BOT_END_BEFORE  = int(env_vars['CREATE_BOT_END_BEFORE'])
                cls.LIKE_BOT_START         = int(env_vars['LIKE_BOT_START'])
                cls.LIKE_BOT_END_BEFORE    = int(env_vars['LIKE_BOT_END_BEFORE'])

                LIKE_PAGES_aux = re.sub(r'\s+', "", env_vars['LIKE_PAGES']).split(',')
                LIKE_PAGES_aux = LIKE_PAGES_aux if LIKE_PAGES_aux[-1] != "" else LIKE_PAGES_aux[:-1] # incase last ele ends with ,
                cls.LIKE_PAGES = [page for page in LIKE_PAGES_aux if (page[0] != "#" and page[:2] != "//")] # filter out "comments" eg # and //

            return instance
    # def __init__(self, file=None): # optional
    #         if (file == None):
    #             return
    #         print("GOT A FILE!!!!!!!!")
    #         print("GOT A FILE!!!!!!!!")
    #         print(file)
    #     # if not self._is_initialized:
    #         env_vars = dotenv_values(file)  
    #         self.SELENIUM_IS_HEADLESS   = env_vars['SELENIUM_IS_HEADLESS']
    #         self.ENV                    = env_vars['ENV']
    #         self.EMAIL                  = env_vars['EMAIL']
    #         self.PWORD                  = env_vars['PWORD']
    #         self.CREATE_BOT_START       = int(env_vars['CREATE_BOT_START'])
    #         self.CREATE_BOT_END_BEFORE  = int(env_vars['CREATE_BOT_END_BEFORE'])
    #         self.LIKE_BOT_START         = int(env_vars['LIKE_BOT_START'])
    #         self.LIKE_BOT_END_BEFORE    = int(env_vars['LIKE_BOT_END_BEFORE'])

    #         LIKE_PAGES_aux = re.sub(r'\s+', "", env_vars['LIKE_PAGES']).split(',')
    #         LIKE_PAGES_aux = LIKE_PAGES_aux if LIKE_PAGES_aux[-1] != "" else LIKE_PAGES_aux[:-1] # incase last ele ends with ,
    #         self.LIKE_PAGES = [page for page in LIKE_PAGES_aux if (page[0] != "#" and page[:2] != "//")] # filter out "comments" eg # and //

    #         # self._is_initialized = True  # Set the flag to True after initialization
