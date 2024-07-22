import streamlit as st
import requests
from bs4 import BeautifulSoup
import zipfile
import io
import os

def extract_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()
    except Exception as e:
        return f"Error extracting text from {url}: {str(e)}"

def main():
    st.title("URL Text Extractor")
    
    # User input for URLs
    urls_input = st.text_area("붙여넣기 할 URL들을 입력하세요 (한 줄에 하나씩, 최대 300개):", height=200)
    urls = urls_input.split('\n')
    
    # Limit to 300 URLs
    urls = [url.strip() for url in urls if url.strip()][:300]
    
    if st.button("텍스트 추출 및 압축파일 생성"):
        if not urls:
            st.warning("URL을 입력해주세요.")
            return
        
        # Create a BytesIO object to store the zip file
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for i, url in enumerate(urls):
                text = extract_text_from_url(url)
                filename = f"text_{i+1}.txt"
                zip_file.writestr(filename, text)
        
        # Set the buffer's position to the beginning
        zip_buffer.seek(0)
        
        # Create a download button for the zip file
        st.download_button(
            label="압축파일 다운로드",
            data=zip_buffer,
            file_name="extracted_texts.zip",
            mime="application/zip"
        )
        
        st.success("텍스트 추출 및 압축이 완료되었습니다. 위의 버튼을 클릭하여 다운로드하세요.")

if __name__ == "__main__":
    main()
