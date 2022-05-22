from django.urls import path

from apps.comment.views import setComment, getComment, delComment

urlpatterns = [
    # 发送评论的接口
    path('comment/set/', setComment.as_view()),
    # 获取评论的接口
    path('comment/get/<album_id>/', getComment.as_view()),
    # 删除评论的接口
    path('comment/delete/', delComment.as_view()),
]
