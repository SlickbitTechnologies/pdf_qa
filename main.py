import streamlit as st
from PyPDF2 import PdfReader
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
st.set_page_config(
    page_title='Pdf chat',
    layout='wide'
)
st.header("Pdf QA")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_text_from_pdf(file):
    """Extract text from uploaded PDF file."""
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def generate_response():
    messages = [{
        "role": "system",
        "content":st.session_state.pdf_data
    }]
    history = st.session_state.messages
    if len(history) > 0:
        messages.extend(history)
    print(messages)
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    print(completion.choices[0].message)
    return completion.choices[0].message.content,completion.choices[0].message.role

def on_change():
    st.session_state.messages=[]


with st.sidebar:
    file = st.file_uploader(
        "Upload Pdf file",
        type=["pdf"],
        on_change=on_change
    )
    if file:
        st.toast('File uploaded successfully!', icon='😍')
        # st.balloons()
        # Extract text
        pdf_text = extract_text_from_pdf(file)
        st.session_state.pdf_data = pdf_text
    else:
        st.session_state.pdf_data = None



def initialize_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'pdf_data' not in st.session_state:
        st.session_state.pdf_data = None



def update_ui():

    if st.session_state.pdf_data is None:
        st.write('upload pdf to start chat')
    else:
        prompt = st.chat_input(placeholder="Your message",key='chat_input')
        if prompt:
            st.session_state.messages.append({"role":'user',"content":prompt})
            content,role = generate_response()
            st.session_state.messages.append({"role": role, "content": content})


    print(st.session_state.messages)
    if len(st.session_state.messages) > 0:
        messages = st.session_state.messages
        print(messages)
        for item in messages:
            print(item)
            with st.chat_message(item['role']):
                st.markdown(item['content'])


def main():

    initialize_session_state()

    update_ui()

if __name__ == "__main__":
    main()