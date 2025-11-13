# 문제 해결 가이드

## pydantic-core 빌드 오류 (Python 3.13)

### 증상
```
ERROR: Failed building wheel for pydantic-core
Failed to build pydantic-core
error: failed-wheel-build-for-install
```

### 원인
Python 3.13은 최신 버전이라 일부 패키지들이 사전 빌드된 휠을 제공하지 않을 수 있습니다. `pydantic-core`는 Rust로 작성되어 있어서 컴파일이 필요한데, Rust 컴파일러가 없으면 빌드에 실패합니다.

### 해결 방법

#### 방법 1: 패키지 버전 업데이트 (권장)

이미 `requirements.txt`가 최신 버전으로 업데이트되어 있습니다. 다음 명령어로 다시 설치해보세요:

```bash
# 기존 패키지 제거
pip uninstall pydantic pydantic-core -y

# 캐시 클리어
pip cache purge

# 최신 버전으로 재설치
pip install --upgrade pip
pip install -r requirements.txt
```

#### 방법 2: Python 버전 낮추기 (가장 확실한 방법)

Python 3.11 또는 3.12를 사용하는 것을 권장합니다:

```bash
# pyenv를 사용하는 경우
pyenv install 3.11.9
pyenv local 3.11.9

# 또는 3.12
pyenv install 3.12.7
pyenv local 3.12.7

# 가상환경 재생성
rm -rf venv
python3.11 -m venv venv  # 또는 python3.12
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### 방법 3: Rust 설치 (고급)

Rust를 설치하면 소스에서 컴파일할 수 있습니다:

```bash
# Rust 설치
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 설치 후 터미널 재시작 또는
source $HOME/.cargo/env

# 다시 설치 시도
pip install -r requirements.txt
```

### 확인 방법

```bash
# Python 버전 확인
python --version

# pydantic 설치 확인
python -c "import pydantic; print(pydantic.__version__)"
```

## 기타 일반적인 문제

### 문제: "HF_TOKEN 환경 변수가 설정되지 않았습니다"

**해결**:
```bash
export HF_TOKEN="your_token_here"
```

### 문제: "Invalid username or password"

**해결**: 
1. https://huggingface.co/settings/tokens 에서 토큰 확인
2. 새 토큰 생성 후 환경 변수 업데이트

### 문제: 패키지 버전 충돌

**해결**:
```bash
# 가상환경 재생성
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 문제: macOS에서 권한 오류

**해결**:
```bash
# pip 업그레이드
pip install --upgrade pip --user

# 또는 sudo 사용 (권장하지 않음)
sudo pip install -r requirements.txt
```

## Python 버전별 권장사항

- **Python 3.11**: 가장 안정적, 모든 패키지 지원 ✅ (권장)
- **Python 3.12**: 최신 기능, 대부분의 패키지 지원 ✅
- **Python 3.13**: 최신 버전, 일부 패키지 호환성 문제 가능 ⚠️

## 추가 도움말

문제가 계속되면:
1. Python 버전을 3.11로 낮추기
2. 가상환경 재생성
3. `pip cache purge` 후 재설치

