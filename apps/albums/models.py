from django.db import models

from apps.users.models import User


# 画册
class Albums(models.Model):
    title = models.CharField(max_length=8, verbose_name="画册标题")
    stars = models.IntegerField(default=0, verbose_name="收藏数量")
    comments = models.IntegerField(default=0, verbose_name="评论数量")
    expostitory = models.TextField(verbose_name="画册简介")
    album_type = models.CharField(max_length=8, default="名画", verbose_name="画册类型")
    ispublic = models.BooleanField(default=True, verbose_name="是否公开")
    created_time = models.DateField(auto_now=False, auto_now_add=True, verbose_name="画册创建时间")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="创建者的ID")
    cover_img = models.ImageField(default='group1/M00/00/18/wKixgWKC-MCAOin6AAFipXLsyCU5017204', verbose_name='Pic defaltimg')
    img_list = models.TextField(verbose_name="画册中图片的ID", max_length=500,)

    class Meta:
        db_table = "vgpic_albums"
        verbose_name = "画册"
        verbose_name_plural = verbose_name


# 收藏夹(用户画册中间表)
class UserAlbum(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户ID")
    albums_id = models.ForeignKey(Albums, on_delete=models.CASCADE, verbose_name="画册ID")
    isLike = models.BooleanField(verbose_name="画册ID")

    class Meta:
        db_table = "vgpic_UserAlbum"
        verbose_name = "用户画册中间表"
        verbose_name_plural = verbose_name
