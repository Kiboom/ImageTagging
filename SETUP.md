# 설치 및 설정 가이드

## 1. Hugging Face 토큰 생성

### 토큰이 필요한 이유
Hugging Face의 Inference API를 사용하려면 인증 토큰이 필요합니다. 무료로 생성할 수 있으며, API 사용에 제한이 있지만 개발 및 테스트에는 충분합니다.

### 토큰 생성 단계

1. **Hugging Face 계정 생성**
   - https://huggingface.co/join 에서 무료 계정 생성
   - 이메일 인증 완료

2. **액세스 토큰 생성**
   - https://huggingface.co/settings/tokens 로 이동
   - "New token" 버튼 클릭
   - 토큰 정보 입력:
     - **Name**: `image-recognizer-api` (또는 원하는 이름)
     - **Role**: `read` 선택 (읽기 권한만 필요)
   - "Generate token" 클릭
   - **중요**: 생성된 토큰을 안전한 곳에 복사 (다시 볼 수 없음)

## 2. 로컬 개발 환경 설정

### macOS / Linux

```bash
# 1. 프로젝트 클론
git clone <repository-url>
cd Image-Recognizer

# 2. Python 가상환경 생성 (권장)
python3 -m venv venv
source venv/bin/activate

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 환경 변수 설정
export HF_TOKEN="your_token_here"

# 5. API 서버 실행
python image_tagging_api.py
```

### Windows (PowerShell)

```powershell
# 1. 프로젝트 클론
git clone <repository-url>
cd Image-Recognizer

# 2. Python 가상환경 생성 (권장)
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 환경 변수 설정
$env:HF_TOKEN="your_token_here"

# 5. API 서버 실행
python image_tagging_api.py
```

## 3. 영구적인 환경 변수 설정

### macOS / Linux (bash/zsh)

`.bashrc` 또는 `.zshrc` 파일에 추가:

```bash
# ~/.bashrc 또는 ~/.zshrc
export HF_TOKEN="your_token_here"
```

그 다음:
```bash
source ~/.bashrc  # 또는 source ~/.zshrc
```

### Windows (시스템 환경 변수)

1. "시스템 환경 변수 편집" 검색
2. "환경 변수" 버튼 클릭
3. "사용자 변수" 섹션에서 "새로 만들기" 클릭
4. 변수 이름: `HF_TOKEN`
5. 변수 값: 생성한 토큰
6. "확인" 클릭
7. 터미널 재시작

## 4. Render 배포 설정

### 배포 전 체크리스트
- [ ] GitHub 저장소에 코드 푸시
- [ ] Hugging Face 토큰 생성 완료
- [ ] `render.yaml` 파일 확인

### 배포 단계

1. **Render 계정 생성**
   - https://render.com 에서 무료 계정 생성
   - GitHub 계정 연결

2. **새 Web Service 생성**
   - Dashboard > "New" > "Web Service" 클릭
   - GitHub 저장소 선택

3. **환경 변수 설정** (중요!)
   - "Advanced" 섹션 또는 배포 후 "Environment" 탭
   - "Add Environment Variable" 클릭
   - Key: `HF_TOKEN`
   - Value: 생성한 Hugging Face 토큰 입력
   - "Add" 클릭

4. **배포 시작**
   - "Create Web Service" 클릭
   - 배포 완료까지 약 2-3분 소요

5. **배포 확인**
   - 제공된 URL로 이동 (예: `https://your-app.onrender.com`)
   - `/docs` 엔드포인트에서 API 문서 확인

## 5. 테스트

### API 서버 실행 확인

```bash
# 1. 서버가 실행 중인지 확인
curl http://localhost:8000/health

# 예상 응답:
# {"status": "healthy"}
```

### 이미지 인식 테스트

```bash
# 2. 테스트 스크립트 실행
python test_api.py
```

또는 직접 API 호출:

```bash
curl -X POST "http://localhost:8000/recognize" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://images.unsplash.com/photo-1552053831-71594a27632d"
  }'
```

## 6. 문제 해결

### 문제: "HF_TOKEN 환경 변수가 설정되지 않았습니다"

**원인**: 환경 변수가 설정되지 않았거나 잘못 설정됨

**해결**:
```bash
# 현재 환경 변수 확인
echo $HF_TOKEN  # macOS/Linux
echo $env:HF_TOKEN  # Windows PowerShell

# 값이 없으면 다시 설정
export HF_TOKEN="your_token_here"  # macOS/Linux
$env:HF_TOKEN="your_token_here"  # Windows PowerShell
```

### 문제: "Invalid username or password"

**원인**: Hugging Face 토큰이 유효하지 않음

**해결**:
1. https://huggingface.co/settings/tokens 에서 토큰 확인
2. 토큰이 만료되었거나 삭제된 경우 새로 생성
3. 새 토큰으로 환경 변수 업데이트

### 문제: "모델이 로딩 중입니다" (503 에러)

**원인**: Hugging Face 모델이 처음 로드되는 중

**해결**: 정상적인 동작입니다. 10-30초 후 다시 시도

### 문제: 패키지 설치 오류

**원인**: Python 버전 호환성 문제

**해결**:
```bash
# Python 버전 확인 (3.8 이상 필요)
python --version

# 가상환경 재생성
rm -rf venv
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
pip install --upgrade pip
pip install -r requirements.txt
```

## 7. 보안 주의사항

⚠️ **중요**: Hugging Face 토큰은 비밀로 유지해야 합니다!

- ✅ **권장**:
  - 환경 변수로 관리
  - `.gitignore`에 `.env` 파일 추가
  - Render 등 배포 플랫폼의 환경 변수 기능 사용

- ❌ **절대 하지 말 것**:
  - 코드에 직접 하드코딩
  - GitHub에 토큰 커밋
  - 공개적으로 토큰 공유

## 8. 리소스

- [Hugging Face 문서](https://huggingface.co/docs)
- [HF Inference API 문서](https://huggingface.co/docs/inference-providers/providers/hf-inference)
- [Render 배포 가이드](https://render.com/docs)
- [FastAPI 문서](https://fastapi.tiangolo.com/)

