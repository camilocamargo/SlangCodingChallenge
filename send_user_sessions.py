import requests
from settings import POST_ENDPOINT, HEADERS


class SendUserSession:

    def send_user_session(self, body):
        response = requests.post(POST_ENDPOINT, headers=HEADERS, data=body)
        return response
