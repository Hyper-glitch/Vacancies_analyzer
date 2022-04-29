import os

HH_HEADERS = {'User-Agent': f'{os.environ.get("HH_APP_NAME")}-{os.environ.get("HH_APP_EMAIL")}'}
HH_BASE_API_URL = 'https://api.hh.ru/'
