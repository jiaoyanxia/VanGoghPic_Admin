import json

from django.http import JsonResponse
from django.views import View
from Van_GoghPic_admin.settings import FDFS_BASE_URL
from apps.albums.models import Albums
from apps.comment.models import comment
from apps.users.models import User


class setComment(View):
    def post(self, request, *args, **kwargs):
        print(json.loads(request.body))
        datas = json.loads(request.body)
        user_id = User.objects.get(id=datas['user_id'])
        album_id = Albums.objects.get(id=datas['album_id'])
        try:
            comment.objects.create(uid=user_id,
                                   aid=album_id,
                                   content=datas['text']
                                   )
        except Exception as e:
            print(e)
            return JsonResponse({"code": 400, "errmsg": "发生失败"})
        return JsonResponse({"code": 200, "msg": "OK"})


class getComment(View):
    def get(self, request, album_id):
        try:
            id = Albums.objects.get(id=album_id)
            # 获取所有的评论 按点赞量降序
            comments = list(comment.objects.filter(aid=id).order_by('-like_num').values())
            for i in comments:
                user = User.objects.get(id=i["uid_id"])
                i["username"] = user.username
                i["author_img"] = FDFS_BASE_URL + str(user.author_img)
        except Exception as e:
            # print(e)
            return JsonResponse({"code": 400, "msg": "获取评论失败"})
        return JsonResponse({"code": 200, "msg": "OK", "data": comments})


class delComment(View):
    def post(self, request, *args, **kwargs):
        try:
            comment.objects.get(id=json.loads(request.body)).delete()
        except Exception as e:
            return JsonResponse({"code": 400, "msg": "删除评论失败"})
        return JsonResponse({"code": 200, "msg": "删除评论成功", "data": 222})

