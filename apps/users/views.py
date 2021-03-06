from django.http import JsonResponse
from django.views import View
import json
import time

from django_redis import get_redis_connection
from redis import Redis
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from apps.imgs.models import Image
from apps.albums.models import Albums
from apps.users.models import User
from django import http
import re
from django.contrib.auth import login, authenticate

from apps.users.serializers import UserSerializer, UserAllSerializer


class AllCounts(View):
    def get(self, request):
        users = User.objects.all().count()
        albums = Albums.objects.all().count()
        pics = Image.objects.all().count()
        counts = [users, albums, pics]
        return JsonResponse({'code': 200, 'errmsg': 'Get countNum is win', 'data': counts})


class UsernameCountView(View):
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        print(count)
        return JsonResponse({'code': 200, 'errmsg': 'OK', 'count': count})


class MobileCountView(View):
    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        print(count)
        return JsonResponse({'code': 0, 'errmsg': 'OK', 'count': count})


class RegisterView(View):
    def post(self, request):
        json_bytes = request.body  # 从请求体中获取原始的JSON数据，bytes类型的
        json_str = json_bytes.decode()  # 将bytes类型的JSON数据，转成JSON字符串
        json_dict = json.loads(json_str)  # 将JSON字符串，转成python的标准字典

        # 提取参数
        username = json_dict.get('username')
        password = json_dict.get('password')
        password2 = json_dict.get('password2')
        mobile = json_dict.get('mobile')
        sms_code = json_dict.get('sms_code')

        # 判断参数是否齐全
        if not all([username, password, password2, mobile]):
            return http.JsonResponse({'code': 400, 'errmsg': '缺少必传参数!'})
        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_]{5,20}$', username):
            return http.JsonResponse({'code': 400, 'errmsg': 'username格式有误!'})
        # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.JsonResponse({'code': 400, 'errmsg': 'password格式有误!'})
        # 判断两次密码是否一致
        if password != password2:
            return http.JsonResponse({'code': 400, 'errmsg': '两次输入不对!'})
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.JsonResponse({'code': 400, 'errmsg': 'mobile格式有误!'})

        redis: Redis = get_redis_connection('code')
        sms_code_redis = redis.get('smscode_%s' % mobile)
        print(sms_code_redis)
        if not sms_code_redis:
            return JsonResponse({'code': 400, 'errmsg': '验证码过期'})
        sms_code_redis = sms_code_redis.decode()
        if sms_code != sms_code_redis:
            return JsonResponse({'code': 400, 'errmsg': '验证码输入错误'})

        try:
            user = User.objects.create_user(username=username,
                                            password=password,
                                            mobile=mobile)
        except Exception as e:
            return http.JsonResponse({'code': 400, 'errmsg': '注册失败!'})
        datalist = {}
        datalist["id"] = user.id
        datalist["username"] = user.username
        token = str(user.mobile)[-1:-5:-1] + user.username[-3:] + str(time.time())[-7:]
        datalist['token'] = token
        login(request, user)
        response = JsonResponse({'code': 200, 'errmsg': 'ok', 'data': datalist})
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)
        return response


class LoginView(View):
    def post(self, request):
        # 1 接收json数据
        body = request.body
        data_dict = json.loads(body)
        username = data_dict.get('username')
        password = data_dict.get('password')

        # 2 验证数据是否为空  正则
        if not all([username, password]):
            return JsonResponse({'code': 400, 'errmsg': '缺少填写数据'})
        import re
        if re.match('^1[3-9]\d{9}$', username):
            User.USERNAME_FIELD = 'mobile'
        else:
            User.USERNAME_FIELD = 'username'

        # 3 验证码用户名和密码是否正确
        user = authenticate(username=username, password=password)
        if not user:
            return JsonResponse({'code': 400, 'errmsg': '用户名密码错误'})
        # 4 状态保持
        login(request, user)
        # 6 返回响应

        us = User.objects.filter(username=user.username).values()
        data = list(us)[0]
        datalist = {}
        datalist["id"] = data["id"]
        datalist["username"] = data["username"]
        token = str(user.mobile)[-1:-5:-1] + user.username[-3:] + str(time.time())[-7:]
        datalist['token'] = token
        response = JsonResponse({'code': 200, 'errmsg': 'ok', 'data': datalist})
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)
        return response


class UserAlbums(ListModelMixin, GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, id):
        b = User.objects.filter(id=id).values()
        return JsonResponse({"code": 200, 'data': b})


class myUser(View):
    def get(self, request, username):
        try:
            user = User.objects.filter(username=username)
            user = UserAllSerializer(user, many=True).data
            data = json.dumps(user)
            if data == '[]':
                return JsonResponse({'code': 400, 'errmsg': '用户不存在'})
        except Exception as e:
            print('error ----- ', e)
            return JsonResponse({'code': 400, 'errmsg': '用户不存在'})
        data = json.loads(data)[0]
        return JsonResponse({'code': 200, 'errmsg': 'OK', 'data': data})


class ReviseUser(View):
    def post(self, request, *args, **kwargs):
        # - 1 接收参数 校验
        datas = json.loads(request.body);
        user = User.objects.get(username=datas['username'])

        try:
            if datas['reimg'] != '':
                user.author_img = datas['reimg'];
            if datas['rename'] != '':
                user.username = datas['rename'];
            if datas['rehobbys'] != '':
                hobby = ';'.join(datas['rehobbys'])
                user.hobby = hobby;
            if datas['remessage'] != '':
                user.signature = datas['remessage'];
        except  Exception as e:
            print(e)
            return JsonResponse({'code': 400, 'errmsg': 'Error'})

        print(user)
        try:
            user.save();
        except Exception as e:
            print(e)
            return JsonResponse({'code': 400, 'errmsg': '服务器出错'})

        # # - 4 返回响应
        # return Response(status=status.HTTP_201_CREATED)
        return JsonResponse({'code': 200, 'errmsg': 'OK', "data": user.username})
