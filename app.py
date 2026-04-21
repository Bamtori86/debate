import random
import time
import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai

st.set_page_config(
    page_title="💡 AI 토론&토의 주제 생성기",
    page_icon="💡",
    layout="centered",
)

# ── Gemini 설정 (Streamlit Secrets에서 키 로드)
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
    AI_AVAILABLE = True
except Exception:
    AI_AVAILABLE = False

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=SUIT:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family:'SUIT','Pretendard','Noto Sans KR',sans-serif !important; }

.stApp { background:linear-gradient(150deg,#EEF2FF 0%,#F0F9FF 45%,#F5F0FF 100%); }

h1 { color:#1E3A8A !important; font-weight:800 !important; font-size:1.9rem !important; letter-spacing:-0.5px; }

/* ── 사이드바 */
[data-testid="stSidebar"] {
    min-width:300px !important; max-width:300px !important;
    background:linear-gradient(160deg,#1E3A8A 0%,#2563EB 60%,#4F46E5 100%) !important;
    border-right:none !important;
    box-shadow:4px 0 24px rgba(37,99,235,0.18);
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div {
    color:rgba(255,255,255,0.92) !important;
    font-size:0.95rem !important;
    font-family:'SUIT',sans-serif !important;
}
[data-testid="stSidebar"] hr { border-color:rgba(255,255,255,0.25) !important; margin:0.7rem 0 !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] > div { gap:0.4rem !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background:rgba(255,255,255,0.12) !important;
    border:1.5px solid rgba(255,255,255,0.25) !important;
    border-radius:10px !important; padding:0.5rem 0.9rem !important;
    transition:all 0.2s !important; cursor:pointer !important; font-weight:600 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background:rgba(255,255,255,0.22) !important;
    border-color:rgba(255,255,255,0.5) !important;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
    background:rgba(255,255,255,0.15) !important;
    border:1.5px solid rgba(255,255,255,0.35) !important;
    border-radius:10px !important; color:white !important;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] svg { fill:white !important; }
[data-testid="stSidebar"] input {
    background:rgba(255,255,255,0.15) !important;
    border:1.5px solid rgba(255,255,255,0.35) !important;
    border-radius:10px !important; color:white !important;
    font-family:'SUIT',sans-serif !important;
}
[data-testid="stSidebar"] input::placeholder { color:rgba(255,255,255,0.5) !important; }
[data-testid="stSidebar"] [data-testid="stSlider"] > div > div > div { background:rgba(255,255,255,0.35) !important; }
[data-testid="stSidebar"] [data-testid="stSlider"] > div > div > div > div { background:white !important; }
[data-testid="stSidebar"] .stButton > button {
    background:white !important; color:#2563EB !important;
    border:none !important; border-radius:12px !important;
    font-weight:800 !important; font-size:1rem !important;
    padding:0.7rem 1rem !important; width:100% !important;
    box-shadow:0 4px 16px rgba(0,0,0,0.15) !important; transition:all 0.2s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background:#EEF2FF !important; transform:translateY(-1px) !important;
    box-shadow:0 6px 20px rgba(0,0,0,0.2) !important;
}
[data-testid="stSidebarCollapsedControl"] {
    background:#2563EB !important; border-radius:0 10px 10px 0 !important;
    box-shadow:3px 0 12px rgba(37,99,235,0.3) !important;
}
[data-testid="stSidebarCollapsedControl"]:hover { background:#1D4ED8 !important; }
[data-testid="stSidebarCollapsedControl"] svg { fill:white !important; }

/* ── AI 모드 배지 */
.ai-mode-bar {
    background:rgba(255,255,255,0.15);
    border:1.5px solid rgba(255,255,255,0.3);
    border-radius:12px;
    padding:0.6rem 0.9rem;
    display:flex; align-items:center; gap:0.5rem;
    margin-top:0.3rem;
}
.ai-dot { width:8px; height:8px; background:#4ADE80; border-radius:50%; flex-shrink:0;
  box-shadow:0 0 6px #4ADE80; animation:pulse 1.8s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
.ai-label { color:white !important; font-size:0.82rem !important; font-weight:700 !important; }

/* ── 선택 요약 카드 */
.summary-card {
    background:linear-gradient(135deg,#1E3A8A,#2563EB);
    border-radius:14px; padding:1rem 1.4rem; margin-bottom:1.2rem;
    display:flex; align-items:center; gap:0.8rem; flex-wrap:wrap;
    box-shadow:0 4px 16px rgba(37,99,235,0.25);
}
.summary-label { color:rgba(255,255,255,0.7); font-size:0.8rem; font-weight:600; letter-spacing:0.3px; }
.summary-chip {
    background:rgba(255,255,255,0.22); border:1.5px solid rgba(255,255,255,0.4);
    color:white; font-size:0.88rem; font-weight:700;
    padding:0.3rem 0.85rem; border-radius:999px;
}
.summary-arrow { color:rgba(255,255,255,0.45); font-size:0.85rem; }
.summary-ai-chip {
    background:linear-gradient(135deg,#F59E0B,#EF4444);
    color:white; font-size:0.72rem; font-weight:800;
    padding:0.2rem 0.6rem; border-radius:999px;
}

/* ── 액션 버튼 */
.stDownloadButton > button {
    background:linear-gradient(135deg,#059669,#0284C7) !important;
    color:white !important; border:none !important; border-radius:12px !important;
    font-weight:700 !important; font-size:0.95rem !important;
    padding:0.65rem 1rem !important; box-shadow:0 4px 14px rgba(5,150,105,0.25) !important;
}

/* ── 안내 박스 */
.welcome-box {
    background:white; border-radius:16px; padding:2.2rem 1.8rem; text-align:center;
    box-shadow:0 2px 12px rgba(37,99,235,0.09); border:1.5px solid #EEF2FF; margin-top:1rem;
}

/* ── 푸터 */
.aion-footer {
    margin-top:2.5rem; padding:1.2rem 1rem; text-align:center;
    border-top:1.5px solid #DCE8FF; color:#94A3B8; font-size:0.8rem; line-height:1.8;
}
.aion-footer strong { color:#2563EB; font-weight:700; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 폴백 DB (AI 실패 시)
# ─────────────────────────────────────────────
FALLBACK_DB = {
    "학급": {
        "토론": [
            "스마트폰을 교실에서 사용할 수 있어야 한다","숙제는 완전히 없애야 한다",
            "학급 회의에서 다수결보다 합의가 우선되어야 한다","교실 자리 배치는 학생이 직접 정해야 한다",
            "시험 성적을 학급 게시판에 공개해도 된다","조별 과제 점수는 개인 점수보다 비중이 커야 한다",
            "학급 청소 당번 제도는 폐지해야 한다","지각 학생에게 벌점을 부여하는 제도는 필요하다",
            "학급 문고 도서는 학생이 직접 선정해야 한다","발표 점수는 자기평가를 50% 반영해야 한다",
        ],
        "토의": [
            "학급 친구들이 서로 존중하는 대화 문화를 만들려면 어떻게 해야 할까?",
            "숙제를 부담 없이 실천할 수 있도록 학급 규칙을 어떻게 바꿀까?",
            "조별 활동에서 무임승차를 줄이기 위한 방법은 무엇일까?",
            "학급 청소를 즐겁고 공평하게 운영하려면 어떤 아이디어가 필요할까?",
            "교실 소음 문제를 줄이기 위해 우리 반이 실천할 수 있는 방법은?",
            "새 학기 전학생이 빠르게 적응하도록 돕는 방법은 무엇일까?",
            "학급 회의 시간을 더 효율적으로 쓰는 운영 방안은?",
            "친구 간 갈등이 생겼을 때 중재 절차를 어떻게 정하면 좋을까?",
            "학급 목표를 정하고 달성 여부를 확인하는 방법은?",
            "칭찬 문화를 학급 안에서 어떻게 만들어갈까?",
        ],
    },
    "학교": {
        "토론": [
            "교복은 자율복으로 대체되어야 한다","학교 매점에서 탄산음료 판매를 금지해야 한다",
            "학교 스포츠클럽 활동은 필수로 운영해야 한다","시험 기간에도 동아리 활동을 유지해야 한다",
            "학교 CCTV 설치를 확대해야 한다","급식 잔반을 줄이기 위해 배식량 선택제를 의무화해야 한다",
            "학교 축제는 학생회가 전권을 가져야 한다","학교 내 휴대폰 수거 제도는 필요하다",
            "학교 도서관은 방과 후에도 개방해야 한다","학교 급식 메뉴 결정에 학생 투표를 반영해야 한다",
        ],
        "토의": [
            "학교 폭력을 예방하기 위해 학생이 주도할 수 있는 활동은 무엇일까?",
            "급식 만족도를 높이기 위한 학생 참여 방식은 어떻게 만들까?",
            "학교 도서관 이용률을 높이기 위한 프로그램 아이디어는?",
            "쉬는 시간 안전사고를 줄이기 위해 어떤 캠페인을 할 수 있을까?",
            "학교 축제를 모두가 즐길 수 있게 기획하려면 무엇이 필요할까?",
            "등교 시간을 더 여유롭게 운영하기 위한 실천 방안은?",
            "학교 내 분리수거 참여율을 높이는 방법은?","학생회와 학급 임원 간 소통 체계를 어떻게 개선할까?",
            "학교 내 갈등 조정을 학생 주도로 운영하려면?","학교 화장실 환경을 개선하기 위한 실천 방안은?",
        ],
    },
    "환경": {
        "토론": [
            "학교에서 일회용품 사용을 전면 금지해야 한다","교내 에어컨 사용 시간을 제한해야 한다",
            "환경 보호를 위해 종이 교과서를 전자책으로 바꿔야 한다","급식에서 고기 메뉴 비중을 줄여야 한다",
            "학교 행사에서 풍선 장식을 금지해야 한다","분리수거를 제대로 하지 않으면 벌점을 주어야 한다",
            "지역 쓰레기 문제 해결에 학생 봉사를 의무화해야 한다","기후 위기 교육을 정규 교과로 강화해야 한다",
            "친환경 제품 사용을 위해 추가 비용을 감수해야 한다","탄소 중립 실천 서약을 학교 전체가 해야 한다",
        ],
        "토의": [
            "우리 학교에서 일회용품을 줄이려면 어떻게 해야 할까?",
            "교실 전기 사용량을 줄이기 위한 실천 계획은 무엇일까?",
            "등하굣길 탄소 배출을 줄이기 위한 아이디어는?",
            "학교 텃밭 활동을 지속 가능하게 운영하려면 어떤 역할 분담이 필요할까?",
            "환경 동아리와 일반 학생이 함께할 수 있는 캠페인은?",
            "잔반 줄이기 목표를 달성하기 위한 학급별 실천 방법은?",
            "교내 재활용품 수거를 더 효과적으로 하는 방법은?",
            "기후 위기 인식 개선을 위한 학생 참여 프로젝트는 무엇일까?",
            "학교 주변 환경 정화 활동을 꾸준히 유지하는 방법은?",
            "빗물 재활용 등 학교에서 실천할 수 있는 물 절약 방안은?",
        ],
    },
    "사회": {
        "토론": [
            "청소년도 지역 정책 결정에 투표할 권리가 있어야 한다",
            "학교 봉사활동 시간을 졸업 필수 요건으로 유지해야 한다",
            "가짜 뉴스 유포에 대해 강한 처벌이 필요하다","공공장소에서 개인형 이동장치 이용을 제한해야 한다",
            "청소년의 야간 학원 이용 시간을 제한해야 한다","SNS 실명제를 도입해야 한다",
            "청소년도 일정 소득이 있으면 세금을 내야 한다","지역사회 봉사는 오프라인이 우선되어야 한다",
            "미디어 리터러시 교육은 의무 교과가 되어야 한다","청소년 선거 연령을 더 낮춰야 한다",
        ],
        "토의": [
            "가짜 뉴스에 속지 않기 위해 학생이 실천할 수 있는 검증 방법은?",
            "지역사회 문제를 학교 수업과 연결해 해결하려면 어떤 활동이 좋을까?",
            "온라인에서의 혐오 표현을 줄이기 위한 학교 캠페인 아이디어는?",
            "교통약자를 배려하는 등하굣길 문화를 만들려면 어떻게 할까?",
            "학생들이 지역 봉사활동에 자발적으로 참여하도록 만드는 방법은?",
            "디지털 시민성을 키우기 위한 학급 프로젝트 주제는 무엇일까?",
            "학교 밖 청소년과 함께하는 연계 활동을 기획한다면?",
            "세대 간 소통을 돕는 지역사회 프로그램 아이디어는?",
            "지역 어르신과 학생이 함께하는 교류 프로그램을 어떻게 만들까?",
            "학생이 직접 지역 문제를 찾고 해결책을 제안하는 방법은?",
        ],
    },
    "동물": {
        "토론": [
            "반려동물 구매보다 입양을 의무화해야 한다","동물원은 교육 목적이라도 폐지해야 한다",
            "유기동물 보호를 위해 반려동물 등록제를 강화해야 한다","동물 실험은 의학 발전을 위해 허용되어야 한다",
            "학교에서 동물 체험 수업을 금지해야 한다","길고양이 급식소 설치를 지자체가 의무 지원해야 한다",
            "반려동물 동반 공공시설을 확대해야 한다","동물 학대 영상 시청도 처벌 대상에 포함해야 한다",
            "수산시장 활어 판매 방식을 동물 복지 기준에 맞게 바꿔야 한다",
            "동물 복지 등급 표시를 모든 축산물에 의무화해야 한다",
        ],
        "토의": [
            "유기동물 문제를 알리기 위해 학교에서 할 수 있는 활동은?",
            "반려동물과 함께 사는 가정의 책임 문화를 확산하려면 어떻게 할까?",
            "동물 학대 예방 교육을 학생 눈높이에 맞춰 구성하려면?",
            "지역 보호소와 연계한 봉사활동을 지속적으로 운영하는 방법은?",
            "길동물과 주민의 갈등을 줄이기 위한 중재 방안은?",
            "동물을 존중하는 소비 습관을 만드는 실천 방법은?",
            "학교에서 동물 관련 캠페인을 진행할 때 필요한 역할 분담은?",
            "반려동물 유기 예방을 위한 홍보 콘텐츠 아이디어는?",
            "동물원 대신 동물을 배울 수 있는 대안 교육 방법은?",
            "학교 안에서 소동물을 함께 키우는 활동을 어떻게 운영할까?",
        ],
    },
    "과학": {
        "토론": [
            "과학 실험은 가상 시뮬레이션으로 충분하다","학교 과학 수업에서 실험 보고서를 팀 단위로 작성해야 한다",
            "기초과학보다 생활과학 중심 교육이 우선되어야 한다","우주 탐사 연구에 더 많은 예산을 투자해야 한다",
            "유전자 편집 기술은 식량 문제 해결을 위해 적극 활용해야 한다",
            "학교 시험에 과학 계산기 사용을 허용해야 한다","과학 전시회는 모든 학생이 의무 참여해야 한다",
            "과학 수업 평가에서 결과보다 탐구 과정이 더 중요하다",
            "인공지능 연구를 위한 과학 교육을 조기에 시작해야 한다",
            "원자력 에너지는 기후 위기 해결책으로 적극 활용해야 한다",
        ],
        "토의": [
            "과학 탐구 활동을 생활 속 문제 해결과 연결하려면 어떻게 할까?",
            "실험 안전수칙을 학생들이 스스로 지키게 하려면 어떤 방법이 좋을까?",
            "과학 개념이 어려운 친구를 돕는 학급 학습 방법은?",
            "학교 과학실을 더 자주 활용하기 위한 운영 아이디어는?",
            "기후와 에너지 관련 과학 프로젝트를 실천하려면 무엇이 필요할까?",
            "과학 기사 속 정보의 신뢰도를 검증하는 체크리스트를 만든다면?",
            "교내 과학 동아리와 일반 학생이 함께할 수 있는 활동은?",
            "과학 발표 수업에서 협업의 질을 높이는 역할 분담 방식은?",
            "학교 주변 자연환경을 활용한 과학 탐구 활동 아이디어는?",
            "생활 속 과학 원리를 찾는 관찰 일지를 어떻게 운영할까?",
        ],
    },
    "인공지능": {
        "토론": [
            "학교 수업에 AI를 적극 도입해야 한다","생성형 AI 과제 사용은 표절로 보아야 한다",
            "AI 챗봇은 교사의 일부 역할을 대체할 수 있다","학생 맞춤형 AI 학습 분석은 필수 서비스가 되어야 한다",
            "AI 윤리 교육은 코딩 교육보다 먼저 다뤄야 한다","학교 시험에서 AI 도구 사용을 제한해야 한다",
            "학생 개인정보 보호를 위해 AI 학습 앱 사용을 줄여야 한다","AI 기술 발전 속도를 법으로 제한해야 한다",
            "AI가 작성한 글도 저작권을 인정해야 한다","딥페이크 영상 제작 도구는 전면 금지해야 한다",
        ],
        "토의": [
            "AI 도구를 올바르게 사용하는 학급 규칙을 어떻게 만들까?",
            "학생 개인정보를 안전하게 지키기 위한 디지털 습관은?",
            "AI를 활용해 학습 동기를 높이는 수업 아이디어는 무엇일까?",
            "AI 결과물을 비판적으로 검토하는 방법을 학생에게 어떻게 가르칠까?",
            "AI 사용 격차를 줄이기 위해 학교가 지원할 수 있는 방안은?",
            "AI와 함께하는 프로젝트 수업의 공정한 평가 기준은?",
            "허위정보를 생산하는 AI 콘텐츠를 구별하기 위한 실천 방법은?",
            "AI 윤리 이슈를 토의하는 학생 참여 프로그램을 설계한다면?",
            "AI 시대에 인간만이 할 수 있는 역량은 무엇인지 탐색한다면?",
            "학교에서 AI 리터러시를 어떻게 체계적으로 가르칠 수 있을까?",
        ],
    },
    "경제": {
        "토론": [
            "청소년도 용돈 관리 교육을 의무적으로 받아야 한다","학교에서 금융 교육을 정규 교과로 강화해야 한다",
            "현금보다 간편결제 사용이 더 안전하다","중고 거래는 청소년 경제 교육에 도움이 된다",
            "소비자 리뷰는 광고보다 더 신뢰할 수 있다","학생도 친환경 제품 구매를 위해 더 많은 비용을 지불해야 한다",
            "학교 축제 수익금은 전액 기부해야 한다","청소년 아르바이트는 학기 중 제한되어야 한다",
            "용돈 기입장 작성을 학교에서 의무 지도해야 한다","주식 투자 교육을 중학교부터 시작해야 한다",
        ],
        "토의": [
            "합리적인 소비 습관을 기르기 위해 학급에서 할 수 있는 활동은?",
            "용돈을 계획적으로 사용하기 위한 실천 규칙을 만든다면?",
            "학교 행사 예산을 공정하게 배분하는 기준은 무엇일까?",
            "광고와 협찬 콘텐츠를 구별하는 방법을 어떻게 익힐까?",
            "중고 물품 재사용 문화를 학교에 확산시키려면?",
            "학생들이 경제 기사에 관심을 갖게 하는 수업 아이디어는?",
            "소비와 환경을 함께 고려한 구매 체크리스트를 만든다면?",
            "금융 사기 예방을 위해 청소년이 꼭 알아야 할 내용은?",
            "학교 내 미니 장터를 통해 경제 원리를 배우는 방법은?",
            "기부 문화를 학급 안에서 실천하는 방법은 무엇일까?",
        ],
    },
    "문화예술": {
        "토론": [
            "학교 예술 수업 비중을 현재보다 늘려야 한다","대중문화 콘텐츠도 정식 교재로 활용할 수 있다",
            "학교 축제 공연은 오디션으로 선발해야 한다","예술 작품 평가는 점수보다 서술형 피드백이 적절하다",
            "전통문화 교육은 체험 중심으로 바뀌어야 한다","학생 창작물의 온라인 공개는 학교가 장려해야 한다",
            "문화유산 방문 학습은 정기적으로 운영되어야 한다","학교 공연에서 상업성 높은 곡 사용을 제한해야 한다",
            "웹툰·영상 창작도 미술 수업 평가에 포함해야 한다","K-팝 문화 콘텐츠를 정규 교육과정에 반영해야 한다",
        ],
        "토의": [
            "학생들이 예술 활동에 자신감을 갖도록 돕는 수업 방식은?",
            "학교 축제에서 다양한 문화 배경을 반영하려면 어떻게 기획할까?",
            "전통문화 체험 수업을 흥미롭게 운영하는 방법은 무엇일까?",
            "창작 활동에서 서로의 저작권을 존중하는 규칙을 만든다면?",
            "학급 전시회를 모두가 참여할 수 있게 운영하려면?",
            "영화나 음악을 활용한 토의 수업 주제를 어떻게 선정할까?",
            "예술 활동 결과물을 공정하게 평가하는 기준은?",
            "지역 문화시설과 연계한 체험 프로그램 아이디어는?",
            "우리 학교만의 문화 브랜드를 만들려면 무엇이 필요할까?",
            "다문화 배경 학생의 문화를 학교 행사에 녹이는 방법은?",
        ],
    },
    "건강": {
        "토론": [
            "학교에서 체육 수업 시간을 늘려야 한다","학교 급식에서 당분이 높은 음료를 제한해야 한다",
            "청소년 수면 시간을 보장하기 위해 등교 시간을 늦춰야 한다","학교 내 에너지 음료 판매를 금지해야 한다",
            "정신건강 교육은 정규 수업으로 의무화해야 한다",
            "학생 건강 관리를 위해 학교에서 운동 앱 사용을 장려해야 한다",
            "게임 시간 제한은 청소년 건강을 위해 필요하다",
            "학교 급식에 채식 선택권을 의무 제공해야 한다",
            "명상·마음챙김 교육을 학교 정규 시간에 넣어야 한다",
            "학생 체력 검사 결과를 생활기록부에 기재해야 한다",
        ],
        "토의": [
            "학생들의 수면 습관을 개선하기 위해 학급에서 할 수 있는 실천은?",
            "건강한 간식 문화를 만들기 위한 학교 캠페인 아이디어는?",
            "시험 기간 스트레스를 줄이기 위한 자기관리 방법은 무엇일까?",
            "스마트기기 의존을 줄이기 위한 일상 규칙을 어떻게 만들까?",
            "체육 활동에 소극적인 학생도 참여하게 만드는 방법은?",
            "정신건강을 주제로 친구들과 안전하게 대화하는 규칙은?",
            "올바른 자세와 눈 건강을 지키기 위한 교실 환경 개선 아이디어는?",
            "보건실과 연계한 건강 프로젝트를 기획한다면 어떤 주제가 좋을까?",
            "학급 건강 챌린지를 한 달 동안 운영한다면 어떤 활동이 좋을까?",
            "점심 후 쉬는 시간을 건강하게 활용하는 방법은?",
        ],
    },
}


# ─────────────────────────────────────────────
# Gemini AI 생성
# ─────────────────────────────────────────────
def generate_with_gemini(type_key: str, field: str, keyword: str, count: int) -> list:
    if not AI_AVAILABLE:
        return []
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        type_guide = (
            "찬반 논쟁이 가능한 주장문 형태. 반드시 '~해야 한다', '~이다', '~보다 ~이 우선이다' 등으로 끝낼 것."
            if type_key == "토론"
            else "해결 방안을 탐색하는 개방형 질문 형태. 반드시 '~하려면 어떻게 할까?', '~방법은 무엇일까?', '~아이디어는?' 등으로 끝낼 것."
        )
        keyword_clause = f"반드시 키워드 '{keyword}'와 관련된 내용으로 " if keyword.strip() else ""

        prompt = f"""당신은 초등학교·중학교 담임 교사를 돕는 수업 설계 전문가입니다.

[요청]
아래 조건에 맞는 학교 수업용 {type_key} 주제를 정확히 {count}개 생성해주세요.

[조건]
- 유형: {type_key}
- 문장 형식: {type_guide}
- 분야: {field}
- {keyword_clause}학교·학급 생활과 밀접한 현실적인 내용으로 작성
- 초등학교 5~6학년 또는 중학교 1~2학년 수준의 어휘 사용
- 지나치게 추상적이거나 전문적인 표현 지양
- 서로 다른 관점과 주제로 다양하게 구성 (중복 금지)
- 토론이면 찬성/반대 입장이 모두 가능한 주제로 선정

[출력 규칙]
- 주제 텍스트만 출력 (번호, 기호, 설명, 부연 설명 일절 없음)
- 각 주제는 줄바꿈으로만 구분
- 반드시 {count}개 출력

주제:"""

        resp = model.generate_content(prompt)
        raw = resp.text.strip()
        lines = [l.strip() for l in raw.split("\n") if l.strip()]
        cleaned = []
        for line in lines:
            line = line.lstrip("0123456789.-·•*）) ").strip()
            if line:
                cleaned.append(line)
        return cleaned[:count]
    except Exception:
        return []


def generate_from_db(type_key, field, keyword, count):
    if field == "기타":
        pool = []
        for cat in FALLBACK_DB.values():
            pool.extend(cat[type_key])
        random.shuffle(pool)
        if keyword.strip():
            kw = keyword.strip()
            pool = [t for t in pool if kw in t] + [t for t in pool if kw not in t]
        return pool[:min(count, len(pool))]
    pool = list(FALLBACK_DB.get(field, {}).get(type_key, []))
    random.shuffle(pool)
    return pool[:min(count, len(pool))]


def build_download_text(type_key, field, keyword, topics, mode):
    lines = [
        "💡 AI 토론&토의 주제 생성기 결과",
        f"- 유형: {type_key}  /  분야: {field}  /  생성 방식: {mode}",
    ]
    if field == "기타" and keyword.strip():
        lines.append(f"- 키워드: {keyword.strip()}")
    lines += ["", "[생성된 주제]"]
    lines += [f"{i}. {t}" for i, t in enumerate(topics, 1)]
    lines += ["", "ⓒ AI-ON교과연구회. All rights reserved."]
    return "\n".join(lines)


def topic_card_html(idx, badge, topic, gradient):
    safe = topic.replace("\\", "\\\\").replace("'", "\\'").replace('"', "&quot;").replace("\n", " ")
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=SUIT:wght@500;700;800&display=swap');
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:transparent;font-family:'SUIT','Noto Sans KR',sans-serif;padding:2px 0;}}
.card{{background:white;border-radius:14px;padding:0.8rem 1rem;
  display:flex;align-items:center;gap:0.7rem;
  box-shadow:0 2px 12px rgba(37,99,235,0.10);border:1.5px solid #EEF2FF;transition:box-shadow 0.2s;}}
.card:hover{{box-shadow:0 5px 20px rgba(37,99,235,0.18);}}
.num{{color:#1E3A8A;font-weight:800;font-size:1rem;min-width:26px;text-align:center;flex-shrink:0;}}
.badge{{font-size:0.7rem;font-weight:700;color:white;background:{gradient};
  padding:0.2rem 0.55rem;border-radius:999px;white-space:nowrap;flex-shrink:0;}}
.vline{{width:1.5px;height:20px;background:#E2E8F0;flex-shrink:0;}}
.text{{color:#0F172A;font-size:0.93rem;font-weight:500;line-height:1.55;flex:1;}}
.copy-btn{{flex-shrink:0;background:#F0F4FF;color:#2563EB;border:1.5px solid #C7D7FF;
  border-radius:9px;padding:0.35rem 0.8rem;font-size:0.77rem;font-weight:700;cursor:pointer;
  white-space:nowrap;font-family:'SUIT','Noto Sans KR',sans-serif;transition:all 0.18s;}}
.copy-btn:hover{{background:#2563EB;color:white;border-color:#2563EB;}}
.copy-btn.ok{{background:#D1FAE5;color:#065F46;border-color:#6EE7B7;}}
</style></head><body>
<div class="card">
  <span class="num">#{idx}</span>
  <span class="badge">{badge}</span>
  <span class="vline"></span>
  <span class="text">{topic}</span>
  <button class="copy-btn" id="cb{idx}" onclick="doCopy('{safe}','cb{idx}')">📋 복사</button>
</div>
<script>
function doCopy(t,id){{
  var done=function(){{var b=document.getElementById(id);b.classList.add('ok');b.innerHTML='✅ 복사됨';
    setTimeout(function(){{b.classList.remove('ok');b.innerHTML='📋 복사';}},1800);}};
  if(navigator.clipboard){{navigator.clipboard.writeText(t).then(done).catch(function(){{
    var a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();
    document.execCommand('copy');document.body.removeChild(a);done();}});}}
  else{{var a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();
    document.execCommand('copy');document.body.removeChild(a);done();}}
}}
</script></body></html>"""


# ─────────────────────────────────────────────
# Session State 초기화
# ─────────────────────────────────────────────
for k, v in {
    "topics": [], "generated": False,
    "type_key": "", "field": "", "keyword": "", "count": 3, "mode": "",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────
# 헤더
# ─────────────────────────────────────────────
st.title("💡 AI 토론&토의 주제 생성기")
st.caption("학급 토론·토의 수업을 위한 맞춤 주제를 Gemini AI가 생성해드립니다.")

# ─────────────────────────────────────────────
# 사이드바
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:0.4rem 0 0.9rem;'>
      <div style='font-size:1.9rem;'>⚙️</div>
      <div style='font-size:1.05rem;font-weight:800;color:white;letter-spacing:-0.3px;'>주제 설정</div>
      <div style='font-size:0.73rem;color:rgba(255,255,255,0.6);margin-top:0.15rem;'>옵션을 선택하고 생성하세요</div>
    </div>""", unsafe_allow_html=True)

    # AI 상태 표시
    if AI_AVAILABLE:
        st.markdown("""<div class='ai-mode-bar'>
          <div class='ai-dot'></div>
          <span class='ai-label'>Gemini AI 연결됨 · 무한 생성 가능</span>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div style='background:rgba(239,68,68,0.2);border:1.5px solid rgba(239,68,68,0.4);
          border-radius:12px;padding:0.6rem 0.9rem;font-size:0.8rem;color:rgba(255,255,255,0.85);'>
          ⚠️ API 키 미설정 — DB 모드로 동작
        </div>""", unsafe_allow_html=True)

    st.divider()

    st.markdown("<div style='font-size:0.75rem;color:rgba(255,255,255,0.65);font-weight:700;letter-spacing:0.5px;margin-bottom:0.35rem;'>📌 유형</div>", unsafe_allow_html=True)
    selected_type = st.radio("유형", ["🗣️ 토론", "💬 토의"], label_visibility="collapsed")

    st.markdown("<div style='font-size:0.75rem;color:rgba(255,255,255,0.65);font-weight:700;letter-spacing:0.5px;margin:0.75rem 0 0.35rem;'>📂 분야</div>", unsafe_allow_html=True)
    selected_field = st.selectbox(
        "분야",
        ["학급","학교","환경","사회","동물","과학","인공지능","경제","문화예술","건강","기타"],
        label_visibility="collapsed",
    )

    keyword_input = ""
    if selected_field == "기타":
        st.markdown("<div style='font-size:0.75rem;color:rgba(255,255,255,0.65);font-weight:700;letter-spacing:0.5px;margin:0.75rem 0 0.35rem;'>🔍 키워드</div>", unsafe_allow_html=True)
        keyword_input = st.text_input("키워드", placeholder="예: 급식, 독서, 스마트폰...", label_visibility="collapsed")

    st.markdown("<div style='font-size:0.75rem;color:rgba(255,255,255,0.65);font-weight:700;letter-spacing:0.5px;margin:0.75rem 0 0.35rem;'>🎯 생성 개수</div>", unsafe_allow_html=True)
    generate_count = st.slider("개수", 1, 10, 3, label_visibility="collapsed")
    st.markdown(f"<div style='text-align:center;color:white;font-size:0.85rem;font-weight:700;margin-top:-0.2rem;margin-bottom:0.4rem;'>{generate_count}개</div>", unsafe_allow_html=True)

    st.divider()
    generate_btn = st.button("✨ 주제 생성하기", use_container_width=True)


# ─────────────────────────────────────────────
# 생성 로직
# ─────────────────────────────────────────────
type_key = "토론" if "토론" in selected_type else "토의"

def do_generate(tk, fd, kw, cnt):
    topics = []
    mode = "로컬 DB"
    if AI_AVAILABLE:
        with st.spinner("🤖 Gemini AI가 주제를 생성하는 중..."):
            topics = generate_with_gemini(tk, fd, kw, cnt)
            mode = "Gemini AI"
        if not topics:
            st.warning("⚠️ AI 생성 실패 — 로컬 DB로 대체합니다.")
            topics = generate_from_db(tk, fd, kw, cnt)
            mode = "로컬 DB (폴백)"
    else:
        with st.spinner("주제를 불러오는 중..."):
            time.sleep(0.6)
            topics = generate_from_db(tk, fd, kw, cnt)
            mode = "로컬 DB"
    return topics, mode

if generate_btn:
    topics, mode = do_generate(type_key, selected_field, keyword_input, generate_count)
    st.session_state.topics = topics
    st.session_state.generated = True
    st.session_state.type_key = type_key
    st.session_state.field = selected_field
    st.session_state.keyword = keyword_input
    st.session_state.count = generate_count
    st.session_state.mode = mode


# ─────────────────────────────────────────────
# 결과 표시
# ─────────────────────────────────────────────
if not st.session_state.generated:
    st.markdown("""
    <div class="welcome-box">
      <div style='font-size:2.4rem;margin-bottom:0.65rem;'>💡</div>
      <div style='font-size:1.1rem;font-weight:800;color:#1E3A8A;margin-bottom:0.5rem;'>주제를 생성해보세요!</div>
      <div style='font-size:0.9rem;color:#475569;line-height:1.75;'>
        왼쪽 사이드바에서 유형과 분야를 선택한 뒤<br>
        <b style="color:#2563EB;">✨ 주제 생성하기</b> 버튼을 눌러주세요.
      </div>
      <div style='margin-top:1.2rem;padding:0.75rem 1rem;background:#F0F9FF;border-radius:10px;
                  border:1.5px solid #BAE6FD;font-size:0.82rem;color:#0369A1;line-height:1.6;'>
        🤖 <b>Gemini AI 연동</b> — 매번 새롭고 다양한 주제를<br>무한으로 생성합니다.
      </div>
    </div>
    """, unsafe_allow_html=True)
else:
    tk = st.session_state.type_key
    fd = st.session_state.field
    kw = st.session_state.keyword
    topics = st.session_state.topics
    mode = st.session_state.mode

    # 요약 카드
    mode_badge = '<span class="summary-ai-chip">🤖 Gemini AI</span>' if "Gemini" in mode else '<span style="color:rgba(255,255,255,0.6);font-size:0.78rem;">📦 DB</span>'
    kw_part = f'<span class="summary-arrow">›</span><span class="summary-chip">🔍 {kw.strip()}</span>' if fd == "기타" and kw.strip() else ""
    st.markdown(f"""
    <div class="summary-card">
      <span class="summary-label">생성 결과</span>
      <span class="summary-chip">{'🗣️' if tk=='토론' else '💬'} {tk}</span>
      <span class="summary-arrow">›</span>
      <span class="summary-chip">📂 {fd}</span>
      {kw_part}
      {mode_badge}
      <span style="margin-left:auto;color:rgba(255,255,255,0.8);font-size:0.82rem;font-weight:700;">{len(topics)}개</span>
    </div>
    """, unsafe_allow_html=True)

    # 액션 버튼
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔄 다시 생성하기", use_container_width=True, key="regen"):
            new_topics, new_mode = do_generate(tk, fd, kw, st.session_state.count)
            st.session_state.topics = new_topics
            st.session_state.mode = new_mode
            st.rerun()
    with col2:
        if st.button("🗑️ 초기화", use_container_width=True, key="reset"):
            st.session_state.generated = False
            st.session_state.topics = []
            st.rerun()

    st.markdown("")

    # 주제 카드
    gradient = "linear-gradient(135deg,#2563EB,#7C3AED)" if tk == "토론" else "linear-gradient(135deg,#0EA5E9,#6366F1)"
    for idx, topic in enumerate(topics, 1):
        components.html(topic_card_html(idx, tk, topic, gradient), height=66, scrolling=False)

    st.markdown("")
    st.download_button(
        "📥 전체 결과를 TXT로 다운로드",
        data=build_download_text(tk, fd, kw, topics, mode),
        file_name="ai_topic_results.txt",
        mime="text/plain",
        use_container_width=True,
    )

# 푸터
st.markdown("""
<div class="aion-footer">
  <strong>AI-ON교과연구회</strong><br>
  ⓒ 2025 AI-ON교과연구회. All rights reserved.<br>
  본 자료는 교육적 목적으로 제작되었습니다.
</div>
""", unsafe_allow_html=True)
