import os
from docx import Document
import pdfplumber

def get_doc_text(path):
    if os.path.exists(path):
        doc=Document(path)
        text=''
        for para in doc.paragraphs:
            if len(text)>0:
                text=text+'\n'
            text=text+para.text
        return text

def get_pdf_text(path):
    if os.path.exists(path):
        text=''
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                if len(text)>0:
                    text=text+'\n'
                text=text+page.extract_text()
        return text

def get_txt_text(path):
    if os.path.exists(path):
        with open(path,encoding="UTF-8") as file:
            text=file.read()
        return text
