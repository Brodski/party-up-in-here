import random

def rng_wait():
    return random.uniform(.1,3)

class Abstract_State:
    
    save_state_file = None
    
    init = {}
    init['SELENIUM_IS_HEADLESS'] = None
    init['ENV'] = None
    init['EMAIL'] = None
    init['PWORD'] = None
    init['CREATE_BOT_START'] = None
    init['CREATE_BOT_END_BEFORE'] = None
    init['LIKE_BOT_START'] = None
    init['LIKE_BOT_END_BEFORE'] = None
    init['LIKE_PAGES'] = None

    create_state = {}
    create_state['email_index_finished'] = None

    liking_state = {}
    liking_state['email_index_finished'] = None