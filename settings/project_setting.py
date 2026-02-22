import os
from dotenv import load_dotenv

# Determine the environment and load the appropriate .env file
env = os.getenv('env', default='local')

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)

match env:
    case 'cicd':
        dotenv_path = os.path.join(parent_dir, '.env.cicd')
    case 'local':
        dotenv_path = os.path.join(parent_dir, '.env.local')

load_dotenv(dotenv_path)

# Env changed in Jenkins
PROJECT_HOST = os.getenv('host', default=os.getenv('PROJECT_HOST'))

BROWSER_NAME = os.getenv('browser', default=os.getenv('BROWSER_NAME'))
BROWSER_WIDTH = os.getenv('BROWSER_WIDTH')
BROWSER_HEIGHT = os.getenv('BROWSER_HEIGHT')
BROWSER_HEADLESS = os.getenv('BROWSER_HEADLESS')

PW_EXPECT_TIMEOUT = os.getenv('PW_EXPECT_TIMEOUT')
PW_PAGE_TIMEOUT = os.getenv('PW_PAGE_TIMEOUT')
PW_API_TIMEOUT = os.getenv('PW_API_TIMEOUT')

AI_API_KEY = os.getenv('aiApiKey', default=os.getenv('AI_API_KEY'))
TM_LOGIN = os.getenv('TM_LOGIN', default=os.getenv('TM_LOGIN'))
TM_PASSWORD = os.getenv('TM_PASSWORD', default=os.getenv('TM_PASSWORD'))
TM_URL = 'https://app.testomat.io'
