from django.core.files.storage import Storage

from Van_GoghPic_admin import settings
from Van_GoghPic_admin.settings import FDFS_BASE_URL


class FastDFSStorage(Storage):
    # def __init__(self, fdfs_base_url=None):
    #     """
    #     构造方法，可以不带参数，也可以携带参数
    #     :param base_url: Storage的IP
    #     """
    #     self.fdfs_base_url = fdfs_base_url or settings.FDFS_BASE_URL

    def _open(self):
        pass

    def _save(self, name, content, max_length=None):
        pass

    def exists(self, name):
        return False  # 表示文件不存在(可以执行上传)

    def url(self, name):
        # 返回图片的完整路径
        # return self.fdfs_base_url + name
        print("获取图片", FDFS_BASE_URL + name)
        return FDFS_BASE_URL + name
