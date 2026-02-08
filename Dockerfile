FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py . 

# 취약점 테스트를 위한 더미 파일 생성 (Path Traversal 테스트용)
RUN echo "This is a secret system file." > /secret.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
