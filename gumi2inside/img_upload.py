from django.shortcuts import render
import boto3
from django.conf import settings

# 함수에
# from img_upload import img_upload,img_view

# 이미지 올릴 곳에
# from img_upload import img_upload

# 이미지 등록하는 input 넣기
# 형민이가 알려줌

# 이미지 출력 하는 함수 마지막에
# context = img_view(article,context)

# HTML에 
# {% if img_url %}
#   <img src="{{ img_url }}" alt="image" style="max-width: 90%;">
# {% endif %}


def img_upload(request, item):
    file = request.FILES['file']
    status = item.status
    s3_client = boto3.client('s3', 
                            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                            region_name=settings.AWS_S3_REGION_NAME)
    # S3 버킷에 파일 업로드
    s3_path = f"{status}/{file.name}"  # S3 버킷 내 파일 경로
    s3_client.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, s3_path)

    # 업로드한 파일의 S3 URL 생성
    s3_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{s3_path}"
    print(s3_url)
    # User 모델의 img_url 필드에 S3 URL 저장
    item.img_url = s3_url
    print(item.title)
    print(item.img_url)
    item.save()


def img_view(item, context):
    if item.img_url:
        context['img_url'] = item.img_url

    return context







