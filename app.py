import streamlit as st
import openai
import os
from docx import Document
from docx.shared import Inches, Pt
from io import BytesIO
from datetime import datetime

# API-Key setzen
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Volkswirtschaftliche Prognose", page_icon="📈")
st.title("📈 Volkswirtschaftliche Prognose für Regionalbanken")

if st.button("📈 Prognose jetzt generieren und als Word-Datei exportieren"):
    prompt = """
    Erstelle eine volkswirtschaftliche Prognose für die Mittelfristplanung einer kleinen deutschen Regionalbank mit folgenden Bestandteilen:

    1. Erstelle eine Tabelle mit Planungsprämissen zu folgenden Punkten:
       - BIP-Wachstum
       - Inflation (HVPI)
       - Leitzinsen (EZB)
       - Arbeitslosenquote
       - EUR/USD Wechselkurs
       - Energiepreise (Brent, Gas)

    2. Gib für jeden dieser makroökonomischen Cluster eine detaillierte Prognose für die nächsten 3–5 Jahre ab:
       - Bruttoinlandsprodukt (BIP)
       - Inflation (HVPI)
       - Arbeitsmarkt
       - Geldpolitik der EZB
       - Zinsstruktur (Swapkurve)
       - Geopolitische Risiken
       - Auswirkungen auf das Bankgeschäft
       - Wirtschaftliche Risiken

    Verwende professionelle, sachliche Sprache. Gliedere die Abschnitte sauber. Füge Zwischenüberschriften ein. Die Inhalte sollen geeignet für ein Vorstandsgremium sein.
    """

    with st.spinner("Generiere Prognose..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=3000,
            )
            result = response["choices"][0]["message"]["content"]
            st.success("Prognose erfolgreich erstellt!")
            st.markdown(result)

            # Word-Dokument erstellen
            doc = Document()

            # Titelblatt
            doc.add_heading("Volkswirtschaftliche Mittelfristprognose", 0)
            doc.add_paragraph("Erstellt am: " + datetime.now().strftime("%d.%m.%Y"))
            doc.add_paragraph("Zielgruppe: Vorstand und Planungsteam der Regionalbank")
            doc.add_page_break()

            # Inhaltsverzeichnis-Hinweis
            doc.add_paragraph("Inhaltsverzeichnis wird automatisch generiert (in Word aktivieren).")
            doc.add_page_break()

            # Inhalt einfügen (abschnittsweise)
            for section in result.split("\n\n"):
                doc.add_paragraph(section, style='Normal')

            # Formatierung optimieren
            style = doc.styles['Normal']
            font = style.font
            font.name = 'Calibri'
            font.size = Pt(11)

            # Download-Link erzeugen
            buffer = BytesIO()
            doc.save(buffer)
            buffer.seek(0)

            st.download_button(
                label="📄 Word-Bericht herunterladen",
                data=buffer,
                file_name="vwl_prognose.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        except Exception as e:
            st.error(f"Fehler beim Abruf der Prognose: {e}")
