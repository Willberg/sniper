import requests
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from sniper.settings import SESSION_SERVICE


class Authentication(BaseAuthentication):
    """用于用户登录验证"""

    def authenticate(self, request):
        service_url = '%s:%s%s' % (
            SESSION_SERVICE['domain'], str(SESSION_SERVICE['port']), SESSION_SERVICE['service_uri'])
        service_name = SESSION_SERVICE['service_name']
        secret = SESSION_SERVICE['secret']
        headers = {
            'service': service_name,
            'secret': secret
        }

        # 将cookies带上，就可以从am取到session
        cookies = request.COOKIES
        res = requests.post(url=service_url, cookies=cookies, headers=headers).json()
        if not res or not res['status']:
            raise exceptions.AuthenticationFailed('用户未登录')
        # 在rest framework内部会将这两个字段赋值给request，以供后续操作使用
        user_dict = res['data']
        if not user_dict:
            raise exceptions.AuthenticationFailed('用户未登录')

        return user_dict, None

    def authenticate_header(self, request):
        pass
