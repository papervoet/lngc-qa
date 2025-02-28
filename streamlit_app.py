import streamlit as st
import openai
from openai import OpenAI
from PyPDF2 import PdfReader

# 제목과 설명 표시
st.title("⚓ LNGC 운용 메뉴얼 도우미")
st.write(
    "LNGC 운용 메뉴얼 PDF를 업로드하고 질문해주세요 - GPT AI가 답변해드립니다! "
    "이 앱을 사용하려면 OpenAI API 키가 필요합니다."
)

# OpenAI API 키 입력 받기
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("OpenAI API 키를 입력해주세요.", icon="🗝️")
else:
    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)
    
    # 사용 가능한 모델 목록 표시
    available_models = ["gpt-4", "gpt-4-turbo-preview", "gpt-3.5-turbo"]
    selected_model = st.selectbox(
        "사용할 GPT 모델을 선택하세요",
        available_models
    )

    # PDF 파일 업로더 추가
    uploaded_file = st.file_uploader("LNGC 운용 메뉴얼 PDF 파일을 업로드하세요", type="pdf")
    
    manual_text = ""
    if uploaded_file is not None:
        pdf_reader = PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            manual_text += page.extract_text()
        
        st.success("PDF 파일이 성공적으로 업로드되었습니다!")

    # 사용법 질문 입력 받기
    question = st.text_area(
        "메뉴얼에 대해 궁금한 점을 질문해주세요",
        placeholder="특정 운용 절차나 기술적 방법에 대해 물어보세요",
        disabled=not manual_text,
    )

    if manual_text and question:
        # 메시지 구성
        messages = [
            {"role": "system", "content": "LNGC 운용 메뉴얼에 대한 전문가입니다."},
            {
                "role": "user",
                "content": f"다음은 LNGC 운용 메뉴얼입니다: {manual_text}\n\n질문: {question}\n\n위 메뉴얼 내용을 바탕으로 기술적이고 상세한 답변을 제공해주세요."
            }
        ]

        # OpenAI API를 통해 답변 생성
        response = client.chat.completions.create(
            model=selected_model,
            messages=messages,
            max_tokens=1000
        )

        # 답변 표시
        st.write(response.choices[0].message.content)
