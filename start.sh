#!/bin/bash

# Render.com에서 제공하는 PORT 환경 변수 사용, 없으면 기본값 10000 사용
PORT=${PORT:-10000}

# 모든 네트워크 인터페이스에서 수신 대기
exec uvicorn image_tagging_api:app --host 0.0.0.0 --port $PORT 