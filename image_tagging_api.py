from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
import requests
from typing import List, Dict, Optional

app = FastAPI(
    title="Image Recognition API",
    description="이미지 인식 API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ImageRequest(BaseModel):
    image_url: HttpUrl
    token: Optional[str] = None

class RecognitionResult(BaseModel):
    label: str
    score: float

class ImageResponse(BaseModel):
    success: bool
    results: List[RecognitionResult]
    message: str = ""

# Hugging Face Inference API 설정
# 문서: https://huggingface.co/docs/inference-providers/providers/hf-inference
HF_MODEL = "microsoft/resnet-50"
HF_API_BASE_URL = "https://router.huggingface.co/hf-inference/models"

def get_token(token: Optional[str] = None) -> str:
    """
    Hugging Face API 토큰 검증
    
    Args:
        token: Hugging Face API 토큰
    
    Returns:
        API 토큰 문자열
    """
    if not token:
        raise HTTPException(
            status_code=400,
            detail="토큰이 제공되지 않았습니다. 요청 파라미터로 token을 전달해주세요."
        )
    return token

def download_image(image_url: str) -> tuple[bytes, str]:
    """
    이미지 URL에서 이미지 다운로드
    
    Args:
        image_url: 이미지 URL
    
    Returns:
        (이미지 바이너리 데이터, Content-Type) 튜플
    """
    try:
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        image_data = response.content
        content_type = response.headers.get("Content-Type", "image/jpeg").split(";")[0].strip()
        return image_data, content_type
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"이미지 다운로드 실패: {str(e)}")

def call_hugging_face_api(image_data: bytes, content_type: str, token: str) -> requests.Response:
    """
    Hugging Face Inference API 호출
    
    Args:
        image_data: 이미지 바이너리 데이터
        content_type: 이미지 Content-Type
        token: API 토큰
    
    Returns:
        API 응답 객체
    """
    api_url = f"{HF_API_BASE_URL}/{HF_MODEL}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": content_type
    }
    return requests.post(api_url, headers=headers, data=image_data, timeout=60)

def parse_api_response(response: requests.Response) -> List[Dict]:
    """
    Hugging Face API 응답 파싱 및 에러 처리
    
    Args:
        response: API 응답 객체
    
    Returns:
        인식 결과 리스트 (label, score 포함)
    """
    if response.status_code == 200:
        result = response.json()
        if not isinstance(result, list):
            result = [result]
        return [
            {
                "label": item.get("label", "") if isinstance(item, dict) else str(item),
                "score": float(item.get("score", 0.0) if isinstance(item, dict) else 0.0)
            }
            for item in result
        ]
    elif response.status_code == 503:
        raise HTTPException(status_code=503, detail="모델이 로딩 중입니다. 잠시 후 다시 시도해주세요.")
    elif response.status_code in (401, 403):
        raise HTTPException(status_code=401, detail="인증 실패: 토큰이 유효하지 않습니다.")
    elif response.status_code == 404:
        raise HTTPException(status_code=404, detail=f"모델을 찾을 수 없습니다: {HF_MODEL}")
    elif response.status_code == 429:
        raise HTTPException(status_code=429, detail="API 사용량 제한에 도달했습니다.")
    else:
        error_text = response.text[:200] if response.text else "Unknown error"
        raise HTTPException(status_code=response.status_code, detail=f"API 오류: {error_text}")

def recognize_image(image_url: str, token: Optional[str] = None) -> List[Dict]:
    """
    Hugging Face API를 사용하여 이미지 인식
    새로운 엔드포인트 사용: router.huggingface.co/hf-inference
    
    Args:
        image_url: 인식할 이미지의 URL
        token: Hugging Face API 토큰 (필수)
    
    Returns:
        인식 결과 리스트 (label, score 포함)
    """
    api_token = get_token(token)
    image_data, content_type = download_image(image_url)
    response = call_hugging_face_api(image_data, content_type, api_token)
    return parse_api_response(response)

@app.get("/")
def read_root():
    """API 상태 확인"""
    return {
        "status": "running",
        "message": "Image Recognition API is running",
        "endpoints": {
            "POST /recognize": "이미지 URL과 토큰(선택적)을 받아 사물 인식"
        }
    }

@app.post("/recognize", response_model=ImageResponse)
async def recognize(request: ImageRequest):
    """
    이미지 URL을 받아서 사물 인식 수행
    
    - **image_url**: 인식할 이미지의 URL (필수)
    - **token**: Hugging Face API 토큰 (필수)
    
    반환값:
    - **success**: 성공 여부
    - **results**: 인식된 객체 목록 (label, score)
    """
    try:
        # 이미지 인식 (URL과 토큰 전달)
        predictions = recognize_image(
            image_url=str(request.image_url),
            token=request.token
        )
        
        # 결과 정리 (상위 5개)
        results = [
            RecognitionResult(label=pred["label"], score=pred["score"])
            for pred in predictions[:5]
        ]
        
        return ImageResponse(
            success=True,
            results=results,
            message="이미지 인식 완료"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"처리 중 오류 발생: {str(e)}")

@app.get("/health")
def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

