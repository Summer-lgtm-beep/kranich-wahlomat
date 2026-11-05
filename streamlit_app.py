import streamlit as st
import requests

st.set_page_config(
    page_title="Was wählen Kraniche?",
    layout="centered"
)

PARTEIEN = ["Die Grünen", "Die Linke", "SPD", "FDP", "CDU", "AfD"]
NAMEN = {"Die Grünen": "Grünen-Kranich", "Die Linke": "Linken-Kranich", "SPD": "SPD-Kranich", "FDP": "FDP-Kranich", "CDU": "CDU-Kranich", "AfD": "AfD-Kranich"}
THESEN = [{"text": "Die Busse und Bahnen der KVG Salzgitter sollten für alle Schülerinnen und Schüler komplett kostenlos sein.", "positionen": [1, 1, 1, -1, -1, 0]}, {"text": "Salzgitter sollte mehr Geld in freies WLAN an Schulen und öffentlichen Plätzen investieren, statt zuerst Schulgebäude zu sanieren.", "positionen": [1, -1, -1, 1, -1, 1]}, {"text": "An Schulen sollte es ein generelles Handyverbot auf dem gesamten Gelände geben, auch in den Pausen.", "positionen": [-1, -1, 0, -1, 1, 1]}, {"text": "Die Stadt sollte mehr Treffpunkte für Jugendliche schaffen, auch wenn dafür weniger Geld für Straßen zur Verfügung steht.", "positionen": [1, 1, 1, 0, -1, -1]}, {"text": "Das Jugendparlament sollte echtes Stimmrecht im Stadtrat erhalten.", "positionen": [1, 1, 1, 1, -1, -1]}, {"text": "Grillen und laute Musik sollten am Salzgittersee und in Parks stärker eingeschränkt werden.", "positionen": [0, -1, -1, -1, 1, 1]}, {"text": "Die Stadt sollte Jugendpartys, Festivals oder eine Disco für Jugendliche finanziell unterstützen.", "positionen": [1, 1, 1, 0, 0, -1]}, {"text": "An Schulkiosken und in Mensen sollte ausschließlich gesundes oder vegetarisches Essen verkauft werden dürfen.", "positionen": [1, 1, 0, -1, -1, -1]}, {"text": "An Kriminalitätsschwerpunkten sollte es mehr Kameras und Videoüberwachung geben.", "positionen": [-1, -1, 1, 1, 1, 1]}, {"text": "Salzgitter sollte mehr Fahrradstraßen bauen, auf denen Autos eingeschränkt sind.", "positionen": [1, 1, 1, -1, -1, -1]}, {"text": "Die Stadt sollte Sportvereine so unterstützen, dass Kinder und Jugendliche kostenlos Mitglied werden können.", "positionen": [1, 1, 1, 0, 0, -1]}, {"text": "Schulen sollten im Unterricht mehr über Klimaschutz und umweltfreundliches Leben behandeln.", "positionen": [1, 1, 1, -1, -1, -1]}]
ANTWORTEN = {"Ich stimme zu": 1, "Neutral": 0, "Ich lehne ab": -1}

if "intro_schritt" not in st.session_state: st.session_state.intro_schritt = 0
if "frage" not in st.session_state: st.session_state.frage = 0
if "antworten" not in st.session_state: st.session_state.antworten = {}
if "fertig" not in st.session_state: st.session_state.fertig = False

def antwort_gewaehlt():
    index = st.session_state.frage
    schluessel = f"auswahl_{index}"
    auswahl = st.session_state.get(schluessel)
    if auswahl not in ANTWORTEN: return
    st.session_state.antworten[index] = ANTWORTEN[auswahl]
    if index < len(THESEN) - 1: st.session_state.frage += 1
    else: st.session_state.fertig = True

def quiz_neustarten():
    for key in list(st.session_state.keys()):
        if key.startswith("auswahl_"): del st.session_state[key]
    st.session_state.frage = 0
    st.session_state.antworten = {}
    st.session_state.fertig = False
    st.session_state.intro_schritt = 0

# ----------------------------------------------------------------------
# DIESE FUNKTION PRÜFT JEDE ENDUNG DIREKT AUF GITHUB AB
# ----------------------------------------------------------------------
def zeige_online_bild(basis_name):
    GITHUB_USER = "Summer-lgtm-beep"
    BASIS_URL = f"https://githubusercontent.com{GITHUB_USER}/kranich-wahlomat/master/"
    
    # Alle denkbaren Endungen, die GitHub angelegt haben könnte
    endungen = [".jpg", ".JPG", ".png", ".PNG", ".jpeg", ".JPEG"]
    
    for endung in endungen:
        test_url = BASIS_URL + basis_name + endung
        # Wir fragen kurz das Internet, ob unter dieser Adresse ein Bild liegt
        antwort = requests.head(test_url)
        if antwort.status_code == 200:
            st.image(test_url, use_container_width=True)
            return
            
    # Falls gar nichts geht, machen wir eine kleine, hübsche Textwarnung statt Absturz
    st.warning(f"Bild '{basis_name}' wurde auf GitHub nicht gefunden. Bitte lade die Datei dort hoch.")

# ==========================================
# INTERAKTIVES INTRO (NUTZT DIE NEUE FUNKTION)
# ==========================================
if st.session_state.intro_schritt == 0:
    zeige_online_bild("banner")
    zeige_online_bild("crowd")
    if st.button("Weiter", use_container_width=True):
        st.session_state.intro_schritt = 1
        st.rerun()
elif st.session_state.intro_schritt == 1:
    zeige_online_bild("intro_text")
    if st.button("Weiter", use_container_width=True):
        st.session_state.intro_schritt = 2
        st.rerun()
elif st.session_state.intro_schritt == 2:
    zeige_online_bild("brief_hinweis")
    if st.button("Postkasten öffnen", use_container_width=True):
        st.session_state.intro_schritt = 3
        st.rerun()
elif st.session_state.intro_schritt == 3:
    zeige_online_bild("brief_zu")
    if st.button("Siegel brechen & öffnen", use_container_width=True):
        st.session_state.intro_schritt = 4
        st.rerun()
elif st.session_state.intro_schritt == 4:
    zeige_online_bild("brief_offen")
    if st.button("Brief schließen & Weiter", use_container_width=True):
        st.session_state.intro_schritt = 5
        st.rerun()
elif st.session_state.intro_schritt == 5:
    zeige_online_bild("start_seite")
    if st.button("JETZT QUIZ STARTEN", use_container_width=True):
        st.session_state.intro_schritt = 6
        st.rerun()

# ==========================================
# DAS QUIZ
# ==========================================
elif st.session_state.intro_schritt == 6 and not st.session_state.fertig:
    index = st.session_state.frage
    these = THESEN[index]
    st.title("Was wählen Kraniche?")
    st.progress((index + 1) / len(THESEN))
    st.write(f"Frage {index + 1} von {len(THESEN)}")
    st.divider()
    st.header(these["text"])
    st.radio("Was ist deine Meinung?", options=list(ANTWORTEN.keys()), index=None, key=f"auswahl_{index}", on_change=antwort_gewaehlt)
else:
    st.title("Dein Ergebnis")
    ergebnisse = {}
    maximale_punkte = len(THESEN) * 2
    for partei_index, partei in enumerate(PARTEIEN):
        punkte = 0
        for frage_index, these in enumerate(THESEN):
            deine_antwort = st.session_state.antworten.get(frage_index, 0)
            partei_antwort = these["positionen"][partei_index]
            if abs(deine_antwort - partei_antwort) == 0: punkte += 2
            elif abs(deine_antwort - partei_antwort) == 1: punkte += 1
        ergebnisse[partei] = punkte / maximale_punkte * 100
    sortiert = sorted(ergebnisse.items(), key=lambda e: e, reverse=True)
    for platz, (partei, prozent) in enumerate(sortiert, start=1):
        st.write(f"{platz}. **{NAMEN[partei]} ({partei})**")
        st.progress(int(round(prozent)))
        st.write(f"{prozent:.1f} % Übereinstimmung")
    st.button("Quiz erneut starten", on_click=quiz_neustarten, use_container_width=True)
