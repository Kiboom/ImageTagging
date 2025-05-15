# fastapi_image_tagging_api.py
# --------------------------------------------------
# 간단한 이미지 URL 기반 태깅 API (FastAPI + PyTorch)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from io import BytesIO
from PIL import Image
import torch
from torchvision import models, transforms
import os
import urllib.request
import ssl

# SSL 인증서 검증 비활성화 (개발 환경용)
ssl._create_default_https_context = ssl._create_unverified_context

# 1. 환경 세팅: imagenet 클래스 파일 다운로드
IMAGENET_LABELS = 'imagenet_classes.txt'
if not os.path.exists(IMAGENET_LABELS):
    urllib.request.urlretrieve(
        'https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt',
        IMAGENET_LABELS
    )

# 2. 모델 로드 (CPU 모드)
model = models.resnet50(pretrained=True)
model.eval()

# 3. 이미지 전처리 파이프라인
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# 4. 레이블 맵 로드
with open(IMAGENET_LABELS, 'r') as f:
    idx2label = [line.strip() for line in f.readlines()]

# 5. FastAPI 앱 정의
app = FastAPI(
    title="Image Tagging API",
    description="이미지 URL을 받아서 ResNet50 기반으로 상위 5개 태그를 추천합니다.",
    version="1.0"
)

class ImageURL(BaseModel):
    image_url: str

@app.post("/tags")
async def get_tags(body: ImageURL):
    # 1) 이미지 다운로드
    try:
        resp = requests.get(body.image_url, timeout=5, verify=False)
        resp.raise_for_status()
        img = Image.open(BytesIO(resp.content)).convert('RGB')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"이미지 다운로드 실패: {e}")

    # 2) 전처리 및 추론
    input_tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        outputs = model(input_tensor)
        probs = torch.nn.functional.softmax(outputs[0], dim=0)
        top5_prob, top5_catid = torch.topk(probs, 5)
        tags = [idx2label[catid] for catid in top5_catid]

    return {"tags": tags}