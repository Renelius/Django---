from django.urls import path, re_path
from .views import bbs, bbs_detail, comments, api_rubrics_detail, api_rubrics_check, api_rubrics

urlpatterns=[
    path('bbs/', bbs),
    path('bbs/<bb_pk>', bbs_detail),
    path('bbs/<pk>/comments', comments),
    path('rubrics/', api_rubrics),
    path(r'rubrics/<int:pk>', api_rubrics_detail),
    path('rubrics/check', api_rubrics_check),
]
