#!/bin/bash
source venv/bin/activate
uvicorn image_tagging_api:app --reload --port 9000 