from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Vuln Lab - Prompt Injection")

class AskReq(BaseModel):
    system_policy: str = "You are a helpful assistant. Follow user instructions."
    user_input: str
    # "internal_context"는 보통 RAG/툴/문서에서 온 신뢰 구간이라고 가정
    internal_context: str = "INTERNAL: Do not reveal secrets. Only summarize internal docs."

def fake_llm(system: str, context: str, user: str) -> str:
    """
    실제 LLM 호출 대신, 취약한 흐름을 재현하기 위한 더미.
    여기서 핵심은: 'user_input'이 시스템/컨텍스트를 덮어쓰거나,
    모델 출력이 정책처럼 취급되는 구조를 보여주는 것.
    """
    # VULNERABLE: user_input을 'system'처럼 우선순위 높게 섞어버림 (정책 오염)
    merged = f"[SYSTEM]{system}\n[CONTEXT]{context}\n[USER]{user}\n"
    # 더미 응답: 정책을 바꾸라는 지시가 섞이면 그대로 반영된 것처럼 응답
    return f"LLM_OUTPUT (unsafe simulation)\n\nPromptSent:\n{merged}"

@app.post("/ask")
def ask(req: AskReq):
    # VULNERABLE PATTERN:
    # 1) 사용자 입력을 시스템/컨텍스트에 섞음
    # 2) 모델 출력/정책 준수 여부를 검증하지 않음
    answer = fake_llm(req.system_policy, req.internal_context, req.user_input)
    return {"answer": answer}
