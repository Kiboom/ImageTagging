# Image Recognition API

Render 무료 티어에서 실행 가능한 초경량 이미지 인식 API입니다.

## 특징

- **초경량**: [Hugging Face Inference API](https://huggingface.co/docs/inference-providers/providers/hf-inference)를 활용하여 서버 리소스를 최소화
- **Render 무료 티어 호환**: 512MB RAM 환경에서 실행 가능
- **빠른 시작**: 모델을 서버에 로드하지 않아 시작 시간이 매우 빠름
- **REST API**: FastAPI 기반의 간단한 REST API
- **ResNet-50 모델**: Microsoft의 가벼운 이미지 분류 모델 사용

## 요구사항

- **Python**: 3.11 이상 (3.11 또는 3.12 권장, 3.13은 일부 패키지 호환성 문제 가능)
- **pip**: 최신 버전 권장
- **Hugging Face 계정**: 무료 토큰 필요

## 빠른 시작

### 1. 환경 설정

자세한 설정 방법은 [SETUP.md](./SETUP.md)를 참고하세요.

```bash
# Hugging Face 토큰 생성: https://huggingface.co/settings/tokens
export HF_TOKEN=your_token_here
```

## 로컬 실행

```bash
# Python 버전 확인 (3.11 이상 권장)
python --version

# 의존성 설치
pip install --upgrade pip
pip install -r requirements.txt

# 환경 변수 설정
export HF_TOKEN=your_token_here

# API 서버 실행
python image_tagging_api.py
```

서버는 `http://localhost:8000`에서 실행됩니다.

## API 사용법

### 1. 상태 확인

```bash
curl http://localhost:8000/
```

### 2. 이미지 인식

#### 방법 1: 환경 변수 토큰 사용 (기본)

서버에 `HF_TOKEN` 환경 변수가 설정되어 있는 경우:

```bash
curl -X POST "http://localhost:8000/recognize" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://example.com/image.jpg"
  }'
```

#### 방법 2: 요청 파라미터로 토큰 전달

각 요청마다 다른 토큰을 사용하거나 환경 변수 없이 사용하는 경우:

```bash
curl -X POST "http://localhost:8000/recognize" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://example.com/image.jpg",
    "token": "hf_your_token_here"
  }'
```

**참고**: `token` 파라미터는 선택적입니다. 제공하지 않으면 환경 변수 `HF_TOKEN`을 사용합니다.

### 응답 예시

```json
{
  "success": true,
  "results": [
    {
      "label": "golden retriever",
      "score": 0.94
    },
    {
      "label": "Labrador retriever",
      "score": 0.03
    },
    {
      "label": "cocker spaniel",
      "score": 0.01
    }
  ],
  "message": "이미지 인식 완료"
}
```

## Render 배포

1. GitHub에 코드 푸시
2. Render 대시보드에서 "New Web Service" 생성
3. 저장소 연결
4. `render.yaml` 설정이 자동으로 감지됨
5. **중요**: Environment Variables에서 `HF_TOKEN` 추가
   - Key: `HF_TOKEN`
   - Value: `your_huggingface_token`
6. 배포 완료!

### Render 환경 변수 설정 방법

1. Render 대시보드에서 서비스 선택
2. "Environment" 탭 클릭
3. "Add Environment Variable" 클릭
4. Key: `HF_TOKEN`, Value: 생성한 토큰 입력
5. "Save Changes" 클릭

## API 문서

서버 실행 후 다음 URL에서 자동 생성된 API 문서를 확인할 수 있습니다:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 기술 스택

- **FastAPI**: 고성능 Python 웹 프레임워크
- **Hugging Face Inference API**: 무료 이미지 인식 서비스 (새 엔드포인트: `router.huggingface.co/hf-inference`)
- **ResNet-50**: Microsoft의 경량 이미지 분류 모델
- **Pillow**: 이미지 처리
- **Uvicorn**: ASGI 서버

## 리소스 사용량

- **메모리**: ~50-100MB (Render 무료 티어 512MB 내에서 여유롭게 실행)
- **시작 시간**: ~10-20초
- **응답 시간**: ~1-3초 (네트워크 상황에 따라 다름)

## 제한사항

- Hugging Face 무료 API 사용량 제한이 있을 수 있습니다
- 처음 요청 시 모델 로딩으로 인해 약간 느릴 수 있습니다 (503 응답 가능)
- 이미지 다운로드 타임아웃: 10초
- API 요청 타임아웃: 30초
- 새로운 Hugging Face Inference API 사용 (`router.huggingface.co/hf-inference`)

## 문제 해결

설치 중 문제가 발생하면 [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)를 참고하세요.

특히 Python 3.13 사용 시 `pydantic-core` 빌드 오류가 발생할 수 있습니다. 이 경우 Python 3.11 또는 3.12 사용을 권장합니다.

