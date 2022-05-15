import json

from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
# from rest_framework.viewsets import ViewSet, ModelViewSet


from apps.albums.models import Albums, UserAlbum
from apps.albums.serializers import AlbumSerializer
from apps.users.models import User
from apps.users.serializers import UserSerializer


class AlbumsView(ListModelMixin, GenericAPIView):
    queryset = Albums.objects.all()
    serializer_class = AlbumSerializer

    def get(self, request):
        return self.list(request)


class SignAlbumView(View):
    def post(self, request, *args, **kwargs):
        list = {}
        datas = json.loads(request.body)
        pid = datas["pid"]
        user_id = datas["user_id"]
        try:
            albumDate = Albums.objects.filter(id=pid).values()
            albumCreator = albumDate[0]['creator_id']
            for (i, v) in albumDate[0].items():
                list[i] = v
            try:
                user = User.objects.get(id=albumCreator)
                s = UserSerializer(user).data
                for (i, v) in s.items():
                    list[i] = v
            except Exception as e:
                print(e)
                return JsonResponse({"code": 400})
        except Exception as e:
            print(e)
            return JsonResponse({"code": 400})

        try:
            user_id = User.objects.get(id=user_id)
            albums_id = Albums.objects.get(id=list['id'])
            # 如果画册关联数据存在
            sea = UserAlbum.objects.get(Q(user_id=user_id.id) & Q(albums_id=albums_id.id));
            print("有收藏过")
            list["isLike"] = sea.isLike
        except:
            print("没有收藏过")
        return JsonResponse({"code": 200, "msg": "OK", 'datalist': list})


class AlbumData(View):
    def get(self, request):
        list = []
        albumDate = Albums.objects.all().values()
        for item in albumDate:
            albumCreator = item['creator_id']
            user = User.objects.get(id=albumCreator)
            s = UserSerializer(user).data
            for (i, v) in s.items():
                item[i] = v
            list.append(item)
        return JsonResponse({"code": 200, 'errmsg': 'Good Job', 'datalist': list})


class createAlbums(View):
    def post(self, request, *args, **kwargs):
        datas = json.loads(request.body);
        user = User.objects.get(username=datas["username"]);
        # {'name': '', 'region': '', 'resource': '公开画册', 'desc': '', 'imgList': [{'uid': 1652102306770}]}

        # 1. 判断是否符合规范
        if len(datas["imgLists"]) < 7:
            return JsonResponse({'code': 400, "errmsg": '最少上传6张图片！'})
        if (datas["title"] and datas["region"] and datas["resource"] and datas["desc"]) == "":
            return JsonResponse({'code': 400, "errmsg": '画册信息填写不完整！'})

        # 2. 处理数据
        # 条件不满足，条件满足
        datas["resource"] = (True, False)[datas["resource"] == "公开画册"];
        datas["imgLists"] = ";".join(datas["imgLists"])
        print(datas["imgLists"])
        # 3. 将数据保存到数据库中
        try:
            alb = Albums.objects.create(title=datas["title"],
                                        album_type=datas["region"],
                                        ispublic=datas["resource"],
                                        expostitory=datas["desc"],
                                        img_list=datas["imgLists"],
                                        cover_img=datas["defaultImg"],
                                        creator_id=user.id)
        except Exception as e:
            print(e)
            return JsonResponse({'code': 400, "errmsg": "服务器错误创建失败"})

        # 返回响应数据
        return JsonResponse({'code': 200, "errmsg": 'OK', "data": alb.id})


class getFavorites(View):
    def post(self, request, *args, **kwargs):
        print(json.loads(request.body))
        datas = json.loads(request.body)
        user_id = User.objects.get(id=datas["user_id"])
        albums_id = Albums.objects.get(id=datas["albunm_id"])
        try:
            try:
                # 如果画册关联数据已经存在
                sea = UserAlbum.objects.get(Q(user_id=user_id) & Q(albums_id=albums_id));
                # sea.isLike = [True, False](sea.isLike == 1)
                sea.isLike = True
                sea.save()
                newOption = sea.isLike
                print("更改关联数据")
            except:
                try:
                    news = UserAlbum.objects.create(user_id=user_id,
                                                    albums_id=albums_id,
                                                    isLike=datas["islike"])
                    newOption = news.isLike
                    print("创建关联数据")
                except Exception as e:
                    print(e)
                    return JsonResponse({'code': 400, "errmsg": "创建失败"})
        except Exception as e:
            return JsonResponse({'code': 400, "errmsg": "服务器错误"})

        print(newOption)
        # 将数据保存到数据库中

        # 返回响应数据
        return JsonResponse({'code': 200, "errmsg": '收藏成功', "data": newOption})


class reFavorites(View):
    def post(self, request, *args, **kwargs):
        datas = json.loads(request.body)
        user_id = User.objects.get(id=datas["user_id"])
        albums_id = Albums.objects.get(id=datas["albunm_id"])
        # 2. 数据获取
        try:
            sea = UserAlbum.objects.get(Q(user_id=user_id) & Q(albums_id=albums_id))
            sea.isLike = False
            sea.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code': 400, "errmsg": 'e'})
        # 返回响应数据
        return JsonResponse({'code': 200, "errmsg": '取消收藏', "data": sea.isLike})


class isFavorites(View):
    def post(self, request, *args, **kwargs):
        datas = json.loads(request.body)
        print(datas)
        user_id = User.objects.get(id=datas["user_id"])
        newList = []
        for i in datas["list"]:
            albums_id = Albums.objects.get(id=i["id"])
            try:
                sea = UserAlbum.objects.get(Q(user_id=user_id.id) & Q(albums_id=albums_id.id))
                if sea.isLike == True:
                    newList.append(i)
            except:
                pass
        # 返回响应数据
        return JsonResponse({'code': 200, "errmsg": '收藏', "data": newList})


class myFavorites(View):
    def post(self, request, *args, **kwargs):
        datas = json.loads(request.body)
        user_id = User.objects.get(id=datas["user_id"])
        list = []
        for i in datas["list"]:
            # print(i["creator_id"])
            # print(user_id)
            if i["creator_id"] == user_id.id:
                list.append(i)
        # 返回响应数据
        return JsonResponse({'code': 200, "errmsg": "我的", "data": list})
