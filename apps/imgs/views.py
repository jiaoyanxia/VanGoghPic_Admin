import json

from django.http import JsonResponse
from django.views import View
from requests import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from Van_GoghPic_admin.settings import FDFS_BASE_URL
from apps.imgs.serializers import TypeSerializer, ImageSerializer
from apps.imgs.models import ImageCategoty, Image


class AllType(GenericAPIView):
    queryset = ImageCategoty.objects.all()
    serializer_class = TypeSerializer

    def get(self, request):
        instance = self.get_queryset().values()
        lists = []
        for i in instance:
            lists.append(i)
        return JsonResponse({"code": 200, "errmsg": 'OK', 'data': lists})


class Images(View):
    def post(self, request, *args, **kwargs):
        datas = json.loads(request.body)
        print("datas", datas)  # {"typeId":1,"PageNum":0,"datas["PageSize"]":50}
        TypeId, PageNum, PageSize = datas["typeId"], datas["PageNum"], datas["PageSize"]
        try:
            imgUrl = Image.objects.filter(category_id=TypeId)
            print("cur", PageSize * PageNum)
            print("per", PageSize * (PageNum + 1))
            dataList = {}  # [PageSize * PageNum: PageSize]
            dataList["imgList"] = list(imgUrl.values())[PageSize * (PageNum + 1): PageSize * PageNum:-1]
            for i in dataList["imgList"]:
                i["image_link"] = FDFS_BASE_URL + i["image_link"]
            # print(dataList["imgList"])
        except Exception as e:
            print(e)
            return JsonResponse({"code": 400, "errmsg": 'The type is Error'})

        dataList["total_num"] = len(imgUrl)
        dataList["typeId"] = TypeId
        return JsonResponse({"code": 200, "errmsg": 'OK', 'data': dataList})


# class Images(View):
#     def post(self, request, *args, **kwargs):
#         id = json.loads(request.body)
#         try:
#             imgUrl = Image.objects.filter(category_id=id)
#             imgList = []
#             for i in imgUrl.values():
#                 imgList.append(i)
#         except Exception as e:
#             print(e)
#             return JsonResponse({"code": 400, "errmsg": 'The type is Error'})
#         imgList = imgList[::-1]
#         return JsonResponse({"code": 200, "errmsg": 'OK', 'data': imgList[:50]})
#

class AllImagesView(ModelViewSet):
    # ?????????
    queryset = Image.objects.all()
    # ????????????
    serializer_class = ImageSerializer

    def update(self, request, *args, **kwargs):
        # - 1 ???????????? ??????
        print(request.data)
        image = request.FILES.get('file')
        print(image)
        # - 2 ??????????????????fastdfs??? ????????????????????????
        from fdfs_client.client import Fdfs_client
        # ??????FastDFS????????????
        client = Fdfs_client('utils/fastdfs/client.conf')
        # ??????
        result = client.upload_by_buffer(image.read())
        print(type(client))
        if result.get("Status") != 'Upload successed.':
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # ?????????fastdfs????????????  ??????????????? ??????????????????
        file_id = result.get("Remote file_id")
        print("file_id", file_id)
        return JsonResponse({'code': 200, 'errmsg': 'OK'})


class userUpdata(View):
    def post(self, request, *args, **kwargs):
        # - 1 ???????????? ??????
        image = request.FILES.get('file')
        # - 2 ??????????????????fastdfs??? ????????????????????????
        from fdfs_client.client import Fdfs_client
        # ??????FastDFS????????????
        client = Fdfs_client('utils/fastdfs/client.conf')
        # ??????
        result = client.upload_by_buffer(image.read())
        if result.get("Status") != 'Upload successed.':
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # ?????????fastdfs????????????  ??????????????? ??????????????????
        file_id = result.get("Remote file_id")
        # print("file_id", file_id)

        # # - 4 ????????????
        return JsonResponse({'code': 200, 'errmsg': 'OK', 'data': file_id})
        # return JsonResponse({'code': 200, 'errmsg': 'OK'})


class UploadImg(View):
    def post(self, request, *args, **kwargs):
        # 1. ??????????????????
        data = json.loads(request.body);
        # print(data["imgList"])
        # length = len(data["imgList"])
        # if length == 0:
        #     return JsonResponse({'code': 400, 'errmsg': '???????????????'})
        # if length > 6:
        #     return JsonResponse({'code': 400, 'errmsg': '????????????6?????????'})
        # 2. ?????????????????????
        for i in data["imgList"]:
            try:
                Image.objects.create(category_id=data["type"], image_link=i);
            except Exception as e:
                print(e)
                return JsonResponse({'code': 400, 'errmsg': '??????????????????'})
        return JsonResponse({'code': 200, 'msg': '??????????????????'})
