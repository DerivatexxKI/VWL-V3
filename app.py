import streamlit as st
import openai
import os

# Konfiguration
st.set_page_config(page_title="Volkswirtschaftlicher Ausblick", page_icon="📊")
st.title("📊 Volkswirtschaftliche Prognose für die Mittelfristplanung")

# OpenAI-API-Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Prompt anzeigen
st.markdown("Die Prognose basiert auf einem vordefinierten Experten-Prompt.")
if st.button("📈 Prognose jetzt generieren"):
    prompt = """
    Du bist ein Ökonom und erstellst eine volkswirtschaftliche Prognose für die Mittelfristplanung einer kleinen deutschen Regionalbank. Gib einen vollständigen Ausblick für die nächsten 3–5 Jahre:

    1. Bruttoinlandsprodukt (BIP)
    2. Inflation (HVPI)
    3. Arbeitsmarkt (Beschäftigung, Arbeitslosenquote)
    4. Geldpolitik der EZB (Leitzinsen, Zinsprognose)
    5. Zinsstruktur (Swapkurve)
    6. Erwartungen zu geopolitischen Risiken
    7. Auswirkungen auf das Bankgeschäft
    8. Wirtschaftliche Risiken

    Bitte professionell und strukturiert antworten, ideal für ein Vorstandsgremium.
    """

    with st.spinner("Generiere volkswirtschaftliche Prognose..."):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1800,
        )
        st.success("Fertig!")
        st.markdown(response.choices[0].message["content"])
