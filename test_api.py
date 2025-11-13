"""
API 테스트 스크립트
로컬에서 API를 실행한 후 이 스크립트로 테스트할 수 있습니다.

사전 요구사항:
1. HF_TOKEN 환경 변수 설정
2. API 서버 실행 (python image_tagging_api.py)
"""

import requests
import json
import os

BASE_URL = "http://localhost:8000"

def test_root():
    """루트 엔드포인트 테스트"""
    print("=== 루트 엔드포인트 테스트 ===")
    response = requests.get(f"{BASE_URL}/")
    print(f"상태 코드: {response.status_code}")
    print(f"응답: {json.dumps(response.json(), indent=2, ensure_ascii=False)}\n")

def test_health():
    """헬스 체크 테스트"""
    print("=== 헬스 체크 테스트 ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"상태 코드: {response.status_code}")
    print(f"응답: {json.dumps(response.json(), indent=2, ensure_ascii=False)}\n")

def test_recognize(image_url, token=None):
    """이미지 인식 테스트"""
    print(f"=== 이미지 인식 테스트 ===")
    print(f"이미지 URL: {image_url}")
    if token:
        print(f"토큰 사용: 파라미터로 전달됨")
    else:
        print(f"토큰 사용: 환경 변수 또는 없음")
    
    payload = {"image_url": image_url}
    if token:
        payload["token"] = token
    
    response = requests.post(
        f"{BASE_URL}/recognize",
        json=payload
    )
    
    print(f"상태 코드: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ 성공: {result['message']}")
        print("\n인식 결과:")
        for i, item in enumerate(result['results'], 1):
            print(f"  {i}. {item['label']}: {item['score']:.4f}")
    else:
        print(f"❌ 실패: {response.text}")
    print()

if __name__ == "__main__":
    print("🚀 API 테스트 시작\n")
    
    # HF_TOKEN 환경 변수 체크 (경고만 표시)
    if not os.getenv("HF_TOKEN"):
        print("⚠️  경고: HF_TOKEN 환경 변수가 설정되지 않았습니다.")
        print("   API 서버가 HF_TOKEN 없이 실행되면 이미지 인식이 실패할 수 있습니다.")
        print("   토큰 생성: https://huggingface.co/settings/tokens\n")
    
    # 기본 엔드포인트 테스트
    test_root()
    test_health()
    
    # 이미지 인식 테스트 (샘플 이미지들)
    sample_images = [
        "https://images.unsplash.com/photo-1552053831-71594a27632d",  # 강아지
        "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba",  # 고양이
        "https://images.unsplash.com/photo-1568572933382-74d440642117",  # 자동차
    ]
    
    # 환경 변수에서 토큰 가져오기 (선택적)
    hf_token = os.getenv("HF_TOKEN")
    
    # 첫 번째 이미지는 환경 변수 토큰 사용 (또는 없으면 토큰 없이)
    test_recognize(sample_images[0], token=None)
    
    # 두 번째 이미지는 파라미터로 토큰 전달 (토큰이 있는 경우)
    if hf_token:
        print("📝 토큰을 파라미터로 전달하는 테스트\n")
        test_recognize(sample_images[1], token=hf_token)
    else:
        print("⚠️  환경 변수에 토큰이 없어 토큰 파라미터 테스트를 건너뜁니다.\n")
        test_recognize(sample_images[1], token=None)
    
    # 세 번째 이미지도 테스트
    test_recognize(sample_images[2], token=None)
    
    print("✅ 모든 테스트 완료!")

