import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

app = FastAPI(title="Vuln Lab - Insecure File Upload")

UPLOAD_DIR = os.path.abspath("./uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_file(f: UploadFile = File(...)):
    # VULNERABLE:
    # 1) filename을 신뢰하여 그대로 저장 (경로 조작 가능)
    # 2) 파일 확장자/콘텐츠 타입/크기 제한 없음
    save_path = os.path.join(UPLOAD_DIR, f.filename)

    content = await f.read()
    with open(save_path, "wb") as out:
        out.write(content)

    return JSONResponse({"saved_to": save_path, "size": len(content)})
