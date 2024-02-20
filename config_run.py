from dotenv import dotenv_values, load_dotenv
import os
import sys

load_dotenv("./.env_config_local")
print(os.getenv("ENV") )
print(os.getenv("ENV") )
print(os.getenv("ENV") )
if os.getenv("ENV") == "local":
    env_vars = dotenv_values('.env_config_local')
elif os.getenv("ENV") == "prod":
    env_vars = dotenv_values('.env_config_prod')
else:
    print("ENV is None! NEED ENV")
    sys.exit(1)  # Exit the script with an error code

for key, value in env_vars.items():
    print(f'{key}: {value}')
SELENIUM_IS_HEADLESS = env_vars['SELENIUM_IS_HEADLESS']
ENV = env_vars['ENV']