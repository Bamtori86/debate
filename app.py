import random
import time
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="💡 AI 토론&토의 주제 생성기",
    page_icon="💡",
    layout="centered",
)

# ── API 설정 및 연결 체크
try:
    import google.generativeai as genai
    # Streamlit Secrets에서 API 키를 가져옵니다.
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
    AI_AVAILABLE = True
except Exception:
    AI_AVAILABLE = False

# [중략: 기존 CSS 스타일 코드와 FALLBACK_DB는 그대로 유지됩니다]

# ... (기존 스타일 및 DB 코드 생략) ...

def generate_with_gemini(type_key, field, keyword, count):
    """Gemini AI로 주제 생성. (topics, mode_str) 튜플 반환."""
    if not AI_AVAILABLE:
        return [], "AI 미연결"
    try:
        # 수정 포인트: 모델명을 'gemini-1.5-flash-latest'로 업데이트하여 404 에러 방지
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        
        type_guide = (
            "찬반 논쟁이 가능한 주장문. 반드시 '~해야 한다', '~이다', '~이 우선이다' 형태로 끝낼 것."
            if type_key == "토론"
            else "해결 방안 탐색 개방형 질문. 반드시 '~어떻게 할까?', '~무엇일까?', '~아이디어는?' 형태로 끝낼 것."
        )
        kw_clause = f"반드시 키워드 '{keyword}'와 관련된 내용으로 " if keyword.strip() else ""
        prompt = f"""당신은 초·중학교 담임 교사를 돕는 수업 설계 전문가입니다.

아래 조건에 맞는 학교 수업용 {type_key} 주제를 정확히 {count}개 생성하세요.

조건:
- 유형: {type_key} / 형식: {type_guide}
- 분야: {field}
- {kw_clause}학교·학급 생활과 밀접한 현실적 내용
- 초등 5~6학년 또는 중1~2 수준 어휘
- 서로 다른 관점으로 다양하게 구성 (중복 금지)

출력 규칙:
- 주제 텍스트만 출력 (번호·기호·설명 없음)
- 줄바꿈으로만 구분
- 반드시 {count}개 출력

주제:"""
        # 버전 호환성을 위해 기본적인 호출 방식 사용
        resp = model.generate_content(prompt)
        raw = resp.text.strip()
        lines = [l.strip() for l in raw.split("\n") if l.strip()]
        cleaned = []
        for line in lines:
            line = line.lstrip("0123456789.-·•*）) ").strip()
            if line:
                cleaned.append(line)
        result = cleaned[:count]
        if result:
            return result, "Gemini AI"
        return [], "빈 응답"
    except Exception as e:
        # 에러 메시지를 더 구체적으로 파악하기 위해 출력
        return [], f"오류:{str(e)[:80]}"

# [이후 나머지 코드(generate_from_db, run_generation 등)는 기존과 동일하게 유지]
