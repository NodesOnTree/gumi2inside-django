from django.urls import path
from . import views

app_name = "challenges"
urlpatterns = [
    # 챌린지 메인 화면, 챌린지 리스트 나옴
    path("", views.challenges_home , name="main"),
    # 새로운 챌린지 생성
    path("create/", views.create_challenge, name="create"),
    # 챌린지 삭제
    path("delete/", views.delete_challenge, name="delete"),
    # 개별 챌린지 확인
    path("detail/", views.detail_challenge, name="detail"),
    # 개별 챌린지 등록
    path("new/", views.new_detail, name="new"),
    # 개별 챌린지 삭제
    path("del/", views.del_detail, name="del"),


    # 챌린지 정보 변경
]