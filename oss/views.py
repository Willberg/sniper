import logging

from django.core.cache import cache
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView

from oss.models import OssDoc
from sniper.constant.content_types import CONTENT_TYPE
from sniper.settings import SNIPER_SERVICE
from sniper.utils.cache import create_key, CACHE_OSS
from sniper.utils.errors import get_error_message, CODE_SYS_PARAMETERS_ERROR, CODE_SYS_MONGO_ERROR, \
    CODE_SNIPER_UPLOAD_URL_EXPIRE, CODE_SYS_UNKNOWN, CODE_SNIPER_FILE_NOT_EXISTS
from sniper.utils.result import Result

log = logging.getLogger('django')


class OssView(APIView):

    # 获取预签名的url
    @staticmethod
    def get(request):
        result = Result()
        content_type = request.GET.get('content_type')
        if not content_type or content_type.lower() not in CONTENT_TYPE.keys():
            result.code = CODE_SYS_PARAMETERS_ERROR
            result.message = get_error_message(result.code)
            return JsonResponse(result.serializer())

        content_type = content_type.lower()

        # 秒为单位
        expire = request.GET.get('expire')
        expire = int(expire) if expire else None

        # 创建过期的key
        try:
            oss_doc = OssDoc()
            oss_doc.content_type = content_type
            od = oss_doc.save()
            upload_url = '%s:%s%s?key=%s' % (
                SNIPER_SERVICE['domain'], str(SNIPER_SERVICE['port']), request.path, str(od.id))
            browse_url = '%s:%s%s?key=%s' % (
                SNIPER_SERVICE['domain'], str(SNIPER_SERVICE['port']), '/api/oss/v1/browse', str(od.id))
            result.data = {
                'key': str(od.id),
                'upload_url': upload_url,
                'browse_url': browse_url
            }

            cache.set(create_key(CACHE_OSS, od.id), content_type, timeout=expire)
        except Exception as e:
            log.error(e)
            result.code = CODE_SYS_MONGO_ERROR
            result.message = get_error_message(result.code)

        return JsonResponse(result.serializer())

    # 上传
    @staticmethod
    def post(request):
        key = request.GET.get('key')
        result = Result()
        if not key:
            result.code = CODE_SYS_PARAMETERS_ERROR
            result.message = get_error_message(result.code)
            return JsonResponse(result.serializer())

        content_type = cache.get(create_key(CACHE_OSS, key))
        if not content_type:
            result.code = CODE_SNIPER_UPLOAD_URL_EXPIRE
            result.message = get_error_message(result.code)
            return JsonResponse(result.serializer())

        # 保存到mongo
        try:
            oss_doc = OssDoc.objects().get(id=key)
            if oss_doc.content_type != content_type:
                result.code = CODE_SYS_UNKNOWN
                result.message = get_error_message(result.code)
                return JsonResponse(result.serializer())

            oss_doc.oss.new_file(content_type=request.FILES['file'].content_type)
            for chunk in request.FILES['file'].chunks():
                oss_doc.oss.write(chunk)
            oss_doc.oss.close()

            od = oss_doc.save()

            # 删除缓存
            cache.delete(create_key(CACHE_OSS, od.id))
            result.data = str(od.id)
        except Exception as e:
            log.error(e)
            result.code = CODE_SYS_MONGO_ERROR
            result.message = get_error_message(result.code)
        return JsonResponse(result.serializer())

    # 删除
    @staticmethod
    def delete(request):
        key = request.GET.get('key')
        result = Result()
        if not key:
            result.code = CODE_SYS_PARAMETERS_ERROR
            result.message = get_error_message(result.code)
            return JsonResponse(result.serializer())

        # 从mongo中取出文件
        result = Result()
        try:
            oss_doc = OssDoc.objects().get(id=key)
        except Exception as e:
            log.debug(e)
            result.code = CODE_SNIPER_FILE_NOT_EXISTS
            result.message = get_error_message(result.code)
            return JsonResponse(result.serializer())

        result.data = str(oss_doc.id)
        oss_doc.delete()
        return JsonResponse(result.serializer())


class OssBrowseView(APIView):

    # 浏览
    @staticmethod
    def get(request):
        key = request.GET.get('key')

        # 从mongo中取出文件
        result = Result()
        try:
            oss_doc = OssDoc.objects().get(id=key)
        except Exception as e:
            log.debug(e)
            result.code = CODE_SNIPER_FILE_NOT_EXISTS
            result.message = get_error_message(result.code)
            return JsonResponse(result.serializer())

        oss = oss_doc.oss.read()
        content_type = CONTENT_TYPE[oss_doc.content_type]
        return HttpResponse(oss, content_type=content_type)
