import json
import re
from time import sleep
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from settings.project_setting import TM_LOGIN, TM_PASSWORD, TM_URL

class BaseApiMethodSingleton(type):
    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super(BaseApiMethodSingleton, cls).__call__(*args, **kwargs)
        return cls.__instances[cls]

class TMMethod(metaclass=BaseApiMethodSingleton):

    def __init__(self) -> None:
        self.session = requests.Session()
        retries = Retry(total=5, backoff_factor=3, status_forcelist=[500, 502])
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("https://", adapter)

        self.csrf_project = None
        self.headers = {"Content-type": "application/json"}
        self.METHOD_GET = "GET"
        self.METHOD_POST = "POST"

    def __send_request(self, method:str, url:str, data:object, headers:object, cookies:object=None,
                     return_resp:bool=True)->object:
        max_retries = 5
        response = None
        for attempt in range(max_retries):
            request = requests.Session()
            retries = Retry(total=5, backoff_factor=10, status_forcelist=[429])
            request.mount("https://", HTTPAdapter(max_retries=retries))
            try:
                if method == self.METHOD_GET and headers:
                    response = self.session.get(url=url, headers=headers, cookies=cookies)
                elif method == self.METHOD_POST:
                    response = self.session.post(url=url, data=data, headers=headers, cookies=cookies)
                break
            except requests.exceptions.RetryError:
                return f"WARNING. Testomat. Limit of url Testomat requests exceeded {url} "
            except requests.exceptions.ConnectionError:
                if attempt == max_retries - 1:
                    return f"WARNING. Testomat. ConnectionError {url} after five retries"
                sleep(5)
        if return_resp:
            return response

    def __get_csrf_token(self, url: str) -> str:
        """Внутрішній метод для отримання CSRF токена з HTML сторінки."""
        response = self.__send_request(method=self.METHOD_GET, url=url, data={},
                                     headers=self.headers)
        token_match = re.search(r'name="csrf-token" content="(.*?)"', response.text)
        if not token_match:
            raise Exception(f"Cannot find csrf-token at: {url}")
        return token_match.group(1)

    def __authenticate(self):
        try:
            login_url = f"{TM_URL}/users/sign_in"
            csrf_login = self.__get_csrf_token(login_url)

            auth_payload = {
                'authenticity_token': csrf_login,
                'user[email]': TM_LOGIN,
                'user[password]': TM_PASSWORD,
                'user[remember_me]': '0',
                'commit': 'Sign In'
            }
            self.__send_request(method=self.METHOD_POST, url=login_url, data=auth_payload,
                              headers={'Content-Type': 'application/x-www-form-urlencoded'})

            project_url = f"{TM_URL}/projects/rotest/"
            self.csrf_project = self.__get_csrf_token(project_url)

        except Exception as e:
            print(f"Помилка авторизації: {e}")
            return None

    def check_content_by_lang(self, page:str, target_lang:str)->str:
        html_page = page.inner_text("body")
        prompt = f"Поверни 'true' якщо в цьому HTML немає неперекладеного тексту іншими мовами крім {target_lang}, '\
            'інакше місця з тестом: {html_page}"

        if self.csrf_project is None:
            self.__authenticate()
        ai_url = f"{TM_URL}/api/rotest/prompts"
        self.headers['X-CSRF-Token'] = self.csrf_project
        ai_payload = {'prompt': 'chat_with_tests', 'message': prompt}
        response = self.__send_request(method=self.METHOD_POST, url=ai_url,
                                       data=json.dumps(ai_payload), headers=self.headers)
        assert response.json().get('text') == 'true'
