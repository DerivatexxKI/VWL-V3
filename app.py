import streamlit as st
import openai
import os
from docx import Document
from docx.shared import Inches, Pt
from io import BytesIO
from datetime import datetime
import pdfplumber

# API-Key setzen
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Volkswirtschaftliche Prognose", page_icon="📈")
st.title("📈 Volkswirtschaftliche Prognose für Regionalbanken")

# Uploadfeld für PDF- oder Word-Dateien
uploaded_files = st.file_uploader(
    "📎 Relevante PDF- oder Word-Dokumente hochladen (optional)",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

# Inhalte aus hochgeladenen Dateien extrahieren
extracted_texts = []
