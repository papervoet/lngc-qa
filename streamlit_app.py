import streamlit as st
import anthropic
from anthropic import Anthropic

# 제목과 설명 표시
st.title("⚓ LNGC 운용 메뉴얼 도우미")
st.write(
    "LNGC 운용 메뉴얼을 입력하고 질문해주세요 - Claude AI가 답변해드립니다! "
    "이 앱을 사용하려면 Anthropic API 키가 필요합니다."
)

# Anthropic API 키 입력 받기
claude_api_key = st.text_input("Anthropic API Key", type="password")
if not claude_api_key:
    st.info("Anthropic API 키를 입력해주세요.", icon="🗝️")
else:
    # Anthropic 클라이언트 생성
    client = Anthropic(api_key=claude_api_key)
    
    # 사용 가능한 모델 목록 표시
    available_models = ["claude-2.1", "claude-2.0", "claude-instant-1.2"]
    selected_model = st.selectbox(
        "사용할 Claude 모델을 선택하세요",
        available_models
    )

    # 메뉴얼 텍스트 입력 받기
    manual_text = st.text_area(
        "LNGC 운용 메뉴얼 내용을 입력하세요",
        height=200
    )

    # 사용법 질문 입력 받기
    question = st.text_area(
        "메뉴얼에 대해 궁금한 점을 질문해주세요",
        placeholder="특정 운용 절차나 기술적 방법에 대해 물어보세요",
        disabled=not manual_text,
    )

    if manual_text and question:
        # 메시지 구성
        messages = [
            {
                "role": "user",
                "content": f"다음은 LNGC 운용 메뉴얼입니다: {manual_text}\n\n질문: {question}\n\n위 메뉴얼 내용을 바탕으로 기술적이고 상세한 답변을 제공해주세요."
            }
        ]

        # Claude API를 통해 답변 생성
        response = client.messages.create(
            model=selected_model,
            messages=messages,
            max_tokens=1000
        )

        # 답변 표시
        st.write(response.content)
