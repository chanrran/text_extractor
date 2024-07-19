import streamlit as st
import requests
from bs4 import BeautifulSoup
import zipfile
import os
from io import BytesIO

# Streamlit 페이지 설정
st.title("URL Text Extractor")
st.write("Please enter a list of URLs (one per line, up to 300 URLs):")

# 입력창
urls = st.text_area("Enter URLs", height=300)
url_list = urls.split()

if st.button("Extract Texts and Download"):
    if len(url_list) > 300:
        st.error("Please enter no more than 300 URLs.")
    else:
        # 폴더 생성
        if not os.path.exists('texts'):
            os.makedirs('texts')

        # 각 URL 처리
        for index, url in enumerate(url_list):
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')

                # 파일 저장
                with open(f'texts/{index+1}.txt', 'w', encoding='utf-8') as file:
                    file.write(soup.get_text())
            except Exception as e:
                st.error(f"Failed to process {url}: {str(e)}")

        # 압축 파일 생성
        with BytesIO() as bio:
            with zipfile.ZipFile(bio, 'w') as zipf:
                for filename in os.listdir('texts'):
                    zipf.write(f'texts/{filename}', filename)
            bio.seek(0)
            
            # 다운로드 링크 제공
            st.download_button(label="Download ZIP File",
                               data=bio,
                               file_name="extracted_texts.zip",
                               mime="application/zip")

        # 임시 파일 삭제
        for filename in os.listdir('texts'):
            os.remove(f'texts/{filename}')
        os.rmdir('texts')
