from rest_framework.authentication import BaseAuthentication
from api import models
from rest_framework.exceptions import AuthenticationFailed

class LuffyAuth(BaseAuthentication):

    def authenticate(self, request):
        """
        用户请求进行认证
        :param request:
        :return:
        """
        # http://wwwww...c0ovmadfasd/?token=adfasdfasdf
        token = request.query_params.get('token')
        obj = models.UserAuthToken.objects.filter(token=token).first()
        if not obj:
            raise AuthenticationFailed({'code':1001,'error':'认证失败'})

        # request.user   request.auth
        #认证通过返回以下元组，后续使用
        return (obj.user.username,obj)