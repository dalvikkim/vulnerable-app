import os
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import FileResponse

app = FastAPI(title="Vuln Lab - Insecure File Download")

BASE_DIR = os.path.abspath("./downloads")
os.makedirs(BASE_DIR, exist_ok=True)

# 샘플 파일 생성
with open(os.path.join(BASE_DIR, "hello.txt"), "w", encoding="utf-8") as f:
    f.write("hello download\n")

@app.get("/download")
def download(file: str = Query(..., description="File path is joined without validation (vulnerable)")):
    # VULNERABLE: path traversal 가능 (검증/정규화/허용목록 없음)
    target = os.path.join(BASE_DIR, file)

    if not os.path.exists(target):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=target, filename=os.path.basename(target))
