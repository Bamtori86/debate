import random
import time

import streamlit as st

st.set_page_config(
    page_title="💡 AI 토론&토의 주제 생성기",
    page_icon="💡",
    layout="centered",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=SUIT:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'SUIT', 'Pretendard', 'Noto Sans KR', sans-serif;
    }
    .stApp {
        background: linear-gradient(135deg, #EEF2FF 0%, #F0F9FF 50%, #F5F3FF 100%);
        min-height: 100vh;
    }

    /* ── 헤더 타이틀 */
    h1 {
        color: #1E3A8A !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
        font-size: 2rem !important;
    }

    /* ── 사이드바 */
    [data-testid="stSidebar"] {
        min-width: 370px !important;
        max-width: 370px !important;
        background: linear-gradient(180deg, #EEF4FF 0%, #F7FAFF 100%) !important;
        border-right: 1.5px solid #C7D7FF !important;
    }
    [data-testid="stSidebar"] * {
        font-size: 1.02rem !important;
    }
    [data-testid="stSidebar"] .stRadio,
    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stTextInput,
    [data-testid="stSidebar"] .stSlider {
        margin-bottom: 0.4rem;
    }

    /* ── 버튼 (생성) */
    .stButton > button {
        background: linear-gradient(135deg, #2563EB, #7C3AED) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 0.65rem 1rem !important;
        transition: all 0.2s ease;
        box-shadow: 0 4px 14px rgba(37,99,235,0.3) !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #1D4ED8, #6D28D9) !important;
        box-shadow: 0 6px 20px rgba(37,99,235,0.45) !important;
        transform: translateY(-1px);
    }

    /* ── 다운로드 버튼 */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #059669, #0284C7) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 0.65rem 1rem !important;
        box-shadow: 0 4px 14px rgba(5,150,105,0.25) !important;
    }
    .stDownloadButton > button:hover {
        opacity: 0.9 !important;
    }

    /* ── 주제 카드 */
    .topic-card {
        background: white;
        border-left: 5px solid;
        border-image: linear-gradient(180deg, #2563EB, #7C3AED) 1;
        border-radius: 12px;
        padding: 1rem 1.4rem;
        margin-bottom: 0.85rem;
        box-shadow: 0 3px 12px rgba(37,99,235,0.10);
        transition: box-shadow 0.2s;
        position: relative;
    }
    .topic-card:hover {
        box-shadow: 0 6px 22px rgba(37,99,235,0.18);
    }
    .topic-header {
        display: flex;
        gap: 0.6rem;
        align-items: center;
        margin-bottom: 0.4rem;
    }
    .topic-number {
        color: #1E3A8A;
        font-weight: 800;
        font-size: 1.05rem;
    }
    .topic-badge {
        display: inline-block;
        font-size: 0.76rem;
        font-weight: 700;
        color: white;
        background: linear-gradient(135deg, #2563EB, #7C3AED);
        padding: 0.18rem 0.65rem;
        border-radius: 999px;
        letter-spacing: 0.3px;
    }
    .topic-text {
        color: #0F172A;
        font-size: 1.02rem;
        line-height: 1.6;
        font-weight: 500;
    }
    .copy-btn {
        margin-top: 0.6rem;
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        background: #F0F4FF;
        color: #2563EB;
        border: 1.5px solid #C7D7FF;
        border-radius: 7px;
        padding: 0.28rem 0.75rem;
        font-size: 0.82rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.18s;
        font-family: 'SUIT', sans-serif;
    }
    .copy-btn:hover {
        background: #2563EB;
        color: white;
        border-color: #2563EB;
    }
    .copy-btn.copied {
        background: #D1FAE5;
        color: #065F46;
        border-color: #6EE7B7;
    }

    /* ── 푸터 */
    .aion-footer {
        margin-top: 3rem;
        padding: 1.2rem 1rem;
        text-align: center;
        border-top: 1.5px solid #DCE8FF;
        color: #64748B;
        font-size: 0.82rem;
        line-height: 1.7;
    }
    .aion-footer strong {
        color: #1E3A8A;
        font-weight: 700;
    }
    </style>

    <script>
    function copyTopic(text, btnId) {
        navigator.clipboard.writeText(text).then(function() {
            var btn = document.getElementById(btnId);
            if (btn) {
                btn.classList.add('copied');
                btn.innerHTML = '✅ 복사됨';
                setTimeout(function() {
                    btn.classList.remove('copied');
                    btn.innerHTML = '📋 복사';
                }, 1800);
            }
        });
    }
    </script>
    """,
    unsafe_allow_html=True,
)

TOPIC_DB = {
    "학급": {
        "토론": [
            "스마트폰을 교실에서 사용할 수 있어야 한다",
            "숙제는 완전히 없애야 한다",
            "학급 회의에서 다수결보다 합의가 우선되어야 한다",
            "교실 자리 배치는 학생이 직접 정해야 한다",
            "시험 성적을 학급 게시판에 공개해도 된다",
            "조별 과제 점수는 개인 점수보다 비중이 커야 한다",
            "학급 청소 당번 제도는 폐지해야 한다",
            "지각 학생에게 벌점을 부여하는 제도는 필요하다",
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
        ],
    },
    "학교": {
        "토론": [
            "교복은 자율복으로 대체되어야 한다",
            "학교 매점에서 탄산음료 판매를 금지해야 한다",
            "학교 스포츠클럽 활동은 필수로 운영해야 한다",
            "시험 기간에도 동아리 활동을 유지해야 한다",
            "학교 CCTV 설치를 확대해야 한다",
            "급식 잔반을 줄이기 위해 배식량 선택제를 의무화해야 한다",
            "학교 축제는 학생회가 전권을 가져야 한다",
            "학교 내 휴대폰 수거 제도는 필요하다",
        ],
        "토의": [
            "학교 폭력을 예방하기 위해 학생이 주도할 수 있는 활동은 무엇일까?",
            "급식 만족도를 높이기 위한 학생 참여 방식은 어떻게 만들까?",
            "학교 도서관 이용률을 높이기 위한 프로그램 아이디어는?",
            "쉬는 시간 안전사고를 줄이기 위해 어떤 캠페인을 할 수 있을까?",
            "학교 축제를 모두가 즐길 수 있게 기획하려면 무엇이 필요할까?",
            "등교 시간을 더 여유롭게 운영하기 위한 실천 방안은?",
            "학교 내 분리수거 참여율을 높이는 방법은 무엇일까?",
            "학생회와 학급 임원 간 소통 체계를 어떻게 개선할까?",
        ],
    },
    "환경": {
        "토론": [
            "학교에서 일회용품 사용을 전면 금지해야 한다",
            "교내 에어컨 사용 시간을 제한해야 한다",
            "환경 보호를 위해 종이 교과서를 전자책으로 바꿔야 한다",
            "급식에서 고기 메뉴 비중을 줄여야 한다",
            "학교 행사에서 풍선 장식을 금지해야 한다",
            "분리수거를 제대로 하지 않으면 벌점을 주어야 한다",
            "지역 쓰레기 문제 해결에 학생 봉사를 의무화해야 한다",
            "기후 위기 교육을 정규 교과로 강화해야 한다",
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
        ],
    },
    "사회": {
        "토론": [
            "청소년도 지역 정책 결정에 투표할 권리가 있어야 한다",
            "학교 봉사활동 시간을 졸업 필수 요건으로 유지해야 한다",
            "가짜 뉴스 유포에 대해 강한 처벌이 필요하다",
            "공공장소에서 개인형 이동장치 이용을 제한해야 한다",
            "청소년의 야간 학원 이용 시간을 제한해야 한다",
            "SNS 실명제를 도입해야 한다",
            "청소년도 일정 소득이 있으면 세금을 내야 한다",
            "지역사회 봉사는 온라인 봉사보다 오프라인이 우선되어야 한다",
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
        ],
    },
    "동물": {
        "토론": [
            "반려동물 구매보다 입양을 의무화해야 한다",
            "동물원은 교육 목적이라도 폐지해야 한다",
            "유기동물 보호를 위해 반려동물 등록제를 강화해야 한다",
            "동물 실험은 의학 발전을 위해 허용되어야 한다",
            "학교에서 동물 체험 수업을 금지해야 한다",
            "길고양이 급식소 설치를 지자체가 의무 지원해야 한다",
            "반려동물 동반 공공시설을 확대해야 한다",
            "동물 학대 영상 시청도 처벌 대상에 포함해야 한다",
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
        ],
    },
    "과학": {
        "토론": [
            "과학 실험은 가상 시뮬레이션으로 충분하다",
            "학교 과학 수업에서 실험 보고서를 팀 단위로 작성해야 한다",
            "기초과학보다 생활과학 중심 교육이 우선되어야 한다",
            "우주 탐사 연구에 더 많은 예산을 투자해야 한다",
            "유전자 편집 기술은 식량 문제 해결을 위해 적극 활용해야 한다",
            "학교 시험에 과학 계산기 사용을 허용해야 한다",
            "과학 전시회는 모든 학생이 의무 참여해야 한다",
            "과학 수업 평가에서 결과보다 탐구 과정이 더 중요하다",
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
        ],
    },
    "인공지능": {
        "토론": [
            "학교 수업에 AI를 적극 도입해야 한다",
            "생성형 AI 과제 사용은 표절로 보아야 한다",
            "AI 챗봇은 교사의 일부 역할을 대체할 수 있다",
            "학생 맞춤형 AI 학습 분석은 필수 서비스가 되어야 한다",
            "AI 윤리 교육은 코딩 교육보다 먼저 다뤄야 한다",
            "학교 시험에서 AI 도구 사용을 제한해야 한다",
            "학생 개인정보 보호를 위해 AI 학습 앱 사용을 줄여야 한다",
            "AI 기술 발전 속도를 법으로 제한해야 한다",
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
        ],
    },
    "경제": {
        "토론": [
            "청소년도 용돈 관리 교육을 의무적으로 받아야 한다",
            "학교에서 금융 교육을 정규 교과로 강화해야 한다",
            "현금보다 간편결제 사용이 더 안전하다",
            "중고 거래는 청소년 경제 교육에 도움이 된다",
            "소비자 리뷰는 광고보다 더 신뢰할 수 있다",
            "학생도 친환경 제품 구매를 위해 더 많은 비용을 지불해야 한다",
            "학교 축제 수익금은 전액 기부해야 한다",
            "청소년 아르바이트는 학기 중 제한되어야 한다",
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
        ],
    },
    "문화예술": {
        "토론": [
            "학교 예술 수업 비중을 현재보다 늘려야 한다",
            "대중문화 콘텐츠도 정식 교재로 활용할 수 있다",
            "학교 축제 공연은 오디션으로 선발해야 한다",
            "예술 작품 평가는 점수보다 서술형 피드백이 적절하다",
            "전통문화 교육은 체험 중심으로 바뀌어야 한다",
            "학생 창작물의 온라인 공개는 학교가 장려해야 한다",
            "문화유산 방문 학습은 정기적으로 운영되어야 한다",
            "학교 공연에서 상업성 높은 곡 사용을 제한해야 한다",
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
        ],
    },
    "건강": {
        "토론": [
            "학교에서 체육 수업 시간을 늘려야 한다",
            "학교 급식에서 당분이 높은 음료를 제한해야 한다",
            "청소년 수면 시간을 보장하기 위해 등교 시간을 늦춰야 한다",
            "학교 내 에너지 음료 판매를 금지해야 한다",
            "정신건강 교육은 정규 수업으로 의무화해야 한다",
            "학생 건강 관리를 위해 학교에서 운동 앱 사용을 장려해야 한다",
            "게임 시간 제한은 청소년 건강을 위해 필요하다",
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
        ],
    },
}


def get_type_key(selected_type_label: str) -> str:
    return "토론" if "토론" in selected_type_label else "토의"


def gather_mixed_topics(type_key: str) -> list:
    mixed = []
    for category in TOPIC_DB.values():
        mixed.extend(category[type_key])
    return mixed


def generate_topics(type_key: str, field: str, keyword: str, count: int) -> list:
    if field == "기타":
        pool = gather_mixed_topics(type_key)
        random.shuffle(pool)
        if keyword.strip():
            keyword_norm = keyword.strip()
            preferred = [t for t in pool if keyword_norm in t]
            others = [t for t in pool if keyword_norm not in t]
            merged = preferred + others
        else:
            merged = pool
        if len(merged) >= count:
            return random.sample(merged, count)
        return merged
    pool = TOPIC_DB[field][type_key]
    if len(pool) >= count:
        return random.sample(pool, count)
    return pool


def build_download_text(type_key: str, field: str, keyword: str, topics: list) -> str:
    lines = [
        "💡 AI 토론&토의 주제 생성기 결과",
        f"- 유형: {type_key}",
        f"- 분야: {field}",
    ]
    if field == "기타":
        lines.append(f"- 키워드: {keyword.strip() if keyword.strip() else '(미입력)'}")
    lines.append("")
    lines.append("[생성된 주제]")
    lines.extend([f"{idx}. {topic}" for idx, topic in enumerate(topics, start=1)])
    lines.append("")
    lines.append("ⓒ AI-ON교과연구회. All rights reserved.")
    return "\n".join(lines)


# ── 헤더
st.title("💡 AI 토론&토의 주제 생성기")
st.caption("학급 토론·토의 수업을 위한 주제를 AI가 추천해드립니다.")

# ── 사이드바
with st.sidebar:
    st.markdown("### ⚙️ 설정")
    st.divider()
    selected_type = st.radio(
        "📌 유형 선택",
        ["🗣️ 토론", "💬 토의"],
    )
    selected_field = st.selectbox(
        "📂 분야 선택",
        ["학급","학교","환경","사회","동물","과학","인공지능","경제","문화예술","건강","기타"],
    )
    keyword_input = ""
    if selected_field == "기타":
        keyword_input = st.text_input(
            "🔍 키워드 입력",
            placeholder="예: 급식, 독서, 스마트폰...",
        )
    generate_count = st.slider("🎯 주제 생성 개수", 1, 10, 3)
    st.divider()
    generate_button = st.button("✨ 주제 생성하기", use_container_width=True)

# ── 메인
if not generate_button:
    st.info("👈 왼쪽 사이드바에서 유형/분야를 선택하고 `✨ 주제 생성하기` 버튼을 눌러보세요.")
else:
    with st.spinner("주제를 생성하는 중입니다..."):
        time.sleep(1.2)

    type_key = get_type_key(selected_type)
    topics = generate_topics(type_key, selected_field, keyword_input, generate_count)

    st.success("✅ 주제 생성 완료!")
    summary_text = (
        f"**선택 요약:** `{type_key}` 유형 · `{selected_field}` 분야"
        + (
            f" · 키워드 `{keyword_input.strip()}`"
            if selected_field == "기타" and keyword_input.strip()
            else ""
        )
    )
    st.markdown(summary_text)
    st.markdown("")

    badge_label = "토론" if type_key == "토론" else "토의"
    for idx, topic in enumerate(topics, start=1):
        btn_id = f"copy_btn_{idx}"
        safe_topic = topic.replace("'", "\\'")
        st.markdown(
            f"""
            <div class="topic-card">
                <div class="topic-header">
                    <span class="topic-number">#{idx}</span>
                    <span class="topic-badge">{badge_label}</span>
                </div>
                <div class="topic-text">{topic}</div>
                <button class="copy-btn" id="{btn_id}"
                    onclick="copyTopic('{safe_topic}', '{btn_id}')">
                    📋 복사
                </button>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    download_text = build_download_text(type_key, selected_field, keyword_input, topics)
    st.download_button(
        "📥 전체 결과를 TXT로 다운로드",
        data=download_text,
        file_name="ai_topic_results.txt",
        mime="text/plain",
        use_container_width=True,
    )

# ── 푸터
st.markdown(
    """
    <div class="aion-footer">
        <strong>AI-ON교과연구회</strong><br>
        ⓒ 2025 AI-ON교과연구회. All rights reserved.<br>
        본 자료는 교육적 목적으로 제작되었습니다.
    </div>
    """,
    unsafe_allow_html=True,
)
