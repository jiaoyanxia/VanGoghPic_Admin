from django.db import models

# Create your models here.
from django.db.models import Model
from apps.albums.models import Albums
from apps.users.models import User


class comment(Model):
    # album_id = models.IntegerField()
    uid = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="评论人的ID")
    aid = models.ForeignKey(Albums, on_delete=models.CASCADE, verbose_name="画册的ID")
    content = models.CharField(max_length=100, verbose_name="评论内容")
    content_time = models.DateField(auto_now_add=True, verbose_name="评论时间")
    like_num = models.IntegerField(default=0, verbose_name="喜欢数量")
    class Meta:
        db_table = "vgpic_comments"
        verbose_name = "评论"
        verbose_name_plural = verbose_name


class commentReply(Model):
    # 评论的ID
    comment_id = models.ForeignKey(comment, on_delete=models.CASCADE, verbose_name="评论的ID")
    # 当前评论的这条回复的ID
    reply_id = models.IntegerField(default=0, verbose_name="回复的ID")
    # commnet ==  第一层回复  ; reply == 回复的回复
    reply_type = models.CharField(default="comment", max_length=10, verbose_name="回复的类型")
    # 发起回复的人
    from_uid = models.IntegerField(default=0, verbose_name="回复用户的ID")
    # 要回复的人
    to_uid = models.IntegerField(default=0, verbose_name="回复目标的ID")
    # 回复的内容
    content = models.CharField(max_length=100, verbose_name="回复的内容")

    class Meta:
        db_table = "vgpic_commentReply"
        verbose_name = "回复"
        verbose_name_plural = verbose_name
