import json
import random

from django.http import HttpResponse, JsonResponse
from django.views import View
from django_redis import get_redis_connection
from redis import Redis
from libs.captcha.captcha import captcha
from utils.smsutils import SmsUtil
from celery_tasks.sms.tasks import send_sms_code

class ImageCodeView(View):
    def get(self, request, uuid):
        text, image = captcha.generate_captcha()
        print(text)
        redis = get_redis_connection('code')
        redis.setex(uuid, 300, text)
        return HttpResponse(image, content_type='image/jpeg')


class SmsView(View):
    def get(self, request, mobile):
        # 校验手机号格式是否正确
        if not mobile:
            return JsonResponse({'code': 300, "errmsg": "手机号为空"})
        # 正则验证
        # 校验图片验证码是否正确
        image_code: str = request.GET.get('image_code')
        print('image_code', image_code)
        image_code_uuid = request.GET.get('image_code_id')
        try:
            # 获取保存都在redis里的图片验证码
            redis: Redis = get_redis_connection('code')
            print(redis)
            image_code_redis = redis.get(image_code_uuid)
            if not image_code_redis:
                return JsonResponse({'code': 400, "errmsg": "验证码过期"})

            image_code_redis = image_code_redis.decode()
            print('image_code_redis', image_code_redis)

            if image_code.lower() != image_code_redis.lower():
                return JsonResponse({'code': 500, "errmsg": "图片验证码错了"})
        except Exception as e:
            print(e)
            return JsonResponse({'code': 600, "errmsg": "网络异常"})

        # 给这个手机号发送短信  第三方
        print("发送短信给", mobile)

        # 先 根据key: flag_手机号 ，获取值
        flag_send = redis.get('flag_%s' % mobile)

        # 如果值存在 ，返回错误响应  过于频繁发送
        if flag_send:
            return JsonResponse({'code': 110, "errmsg": "短信已经发送，请稍后再试"})

        # 生成短信验证码
        sms_code = '%06d' % random.randint(0, 999999)
        print('sms_code=', sms_code)

        # 异步发短信
        print('发短信111')
        send_sms_code.delay(mobile=mobile, code=sms_code)
        print('发短信222')

        # - 创建redis的管道 pipline 对象
        pl = redis.pipeline()
        # - 把redis的操作请求 添加到管道
        pl.setex('smscode_%s' % mobile, 60 * 3, sms_code)
        pl.setex('flag_%s' % mobile, 120, 1)
        # - 执行所有操作
        pl.execute()
        # - 返回响应
        return JsonResponse({'code': 0, "errmsg": "ok"})