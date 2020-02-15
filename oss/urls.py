from django.urls import path

from oss.views import OssView, OssBrowseView

urlpatterns = [
    path('operation', OssView.as_view(), name='oss 相关操作'),

    path('browse', OssBrowseView.as_view(), name='oss 浏览操作'),
]
